'''
Created on 20.08.2024

@author: michael
'''

import os
import time
from posix import system
import sys
import datetime

DEFAULT_BASE = os.path.join("/", "srv", "AudiovisuelleMedien")

class NoFileToTranscribeFound(Exception):
    
    pass

class Logger:
    
    def __init__(self, log_file_name=os.path.join(DEFAULT_BASE, "whisper.log")):
        
        self.log_file = open(log_file_name, "a")
        
    def log(self, message):
        
        now = datetime.datetime.now()
        self.log_file.write("%s: %s\n" % (now.strftime("%Y-%m-%d %H:%M:%S"), message))
        self.log_file.flush()
        print(message)

    def close(self):
        
        self.log("Closing logfile.")
        self.log_file.close()
        
class Crawler:
    
    def __init__(self, logger, start_dir=DEFAULT_BASE):
        
        self.logger = logger
        self.start_dir = start_dir
        self.file_types = (".mp3", ".wav", ".m4v", ".mpg", ".mp4", ".m4a")
        
    def find_next(self):
        for (root, _ ,files) in os.walk(self.start_dir,topdown=False):
            for file in files:
                fullname = os.path.join(root, file)
                if fullname[-4:] in self.file_types:
                    vtt_file = fullname.replace(file[-4:], ".vtt")
                    if not os.path.exists(vtt_file):
                        return fullname
        raise(NoFileToTranscribeFound())
                

if __name__ == '__main__':
    
    
    logger = Logger()

    if len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
        logger.log("Crawling directory %s" % sys.argv[1])
        crawler = Crawler(logger, start_dir=sys.argv[1])
    else:
        logger.log("Crawling default directory")
        crawler = Crawler(logger)
        
    while not os.path.exists(os.path.join(DEFAULT_BASE, "killwhisper")):
        try:
            next_file = crawler.find_next()
            logger.log("Transcribing file %s" % next_file)
            dirname = os.path.dirname(next_file)
            command = 'source /opt/whisper/venv/bin/activate; whisper --language de --model large -f vtt --output_dir \\"%s\\" \\"%s\\"' % (dirname, next_file)
            system('bash -c "%s"' % (command))
            vtt_file_name = os.path.join(dirname, next_file[:-4] + ".vtt")
            if not os.path.exists(vtt_file_name):
                with open(vtt_file_name, "w") as vtt_file:
                    vtt_file.write("Impossible to transcribe file")
            if not os.path.exists(vtt_file_name):
                raise Exception("Can't go on without infinite loop.")
        except NoFileToTranscribeFound:
            logger.log("Nothing more to do. Sleeping for 30 Minutes.")
            time.sleep(60*30) # Sleep for 30 Minutes
    logger.log("Found killfile")
    logger.close()
