#-*- coding: UTF-8 -*-

import unittest
from config import cfg

cfg.test_suite = True


class IndexerTest(unittest.TestCase):

    def testTrue(self):
        self.assertTrue(True)

if __name__ == '__main__':

    unittest.main()