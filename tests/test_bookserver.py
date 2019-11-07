import sys
import unittest

from lib.pyShelf import BookDisplay, BookServer

sys.path.insert(0, '../lib')
sys.path.insert(1, '../')

class BookServerTest(unittest.TestCase):

    def test_bookserver(self):
        server = BookServer()
        self.assertTrue(server.run())

    def test_booksPerPage(self):
        x, y = 900, 450
        self.assertGreater(BookDisplay().booksPerPage([x,y]), 0)
