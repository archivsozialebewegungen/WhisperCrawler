'''
Created on 28.08.2024

@author: michael
'''
import unittest
from Asb.WhisperCrawler.Crawler import Logger, Crawler
import os


class TestCrawler(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testSuspiciousDir(self):
        
        start_dir = os.path.join("/", "srv", "AudiovisuelleMedien", "Sigi")
        logger = Logger(log_file_name=os.path.join("/", "tmp", "test.log"))
        crawler = Crawler(logger, start_dir)
        next_file = crawler.find_next()
        self.assertEqual(next_file, "/srv/AudiovisuelleMedien/Sigi/GrundordnungsversammlungII.m4v")
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()