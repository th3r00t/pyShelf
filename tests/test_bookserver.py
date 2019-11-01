import unittest
import sys
sys.path.insert(0, '../lib')
sys.path.insert(1, '../')
from pyShelf import BookServer

class BookServerTest(unittest.TestCase):

    def test_bookserver(self):
        server = BookServer()
        self.assertTrue(server.run())
