import sys
import unittest

from lib.pyShelf import BookDisplay, BookServer
from lib.display import Frontend
sys.path.insert(0, '../lib')
sys.path.insert(1, '../')

class BookServerTest(unittest.TestCase):

    def __init__(self):
        self.dimensions = [900, 450]

    def test_booksPerPage(self):
        x, y = self.dimensions[0], self.dimensions[1]
        self.assertGreater(BookDisplay().booksPerPage([x,y]), 0)

    def test_Frontend(self):
        x, y = self.dimensions[0], self.dimensions[1]
        ui = Frontend([x, y]).compile("TestCase", "Test Shelf")
        print(ui)
        self.assertNotEqual(ui, False)
