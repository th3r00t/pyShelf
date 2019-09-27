import unittest
from library import Catalogue


class Testing(unittest.TestCase):

    def test_libray_catalogue(self):
        self.assertIsNotNone(Catalogue())

    def test_library_catalogue_filter_books(self):
        self.assertIsNotNone(Catalogue().filter_books())

if __name__ == '__main__':
    unittest.main()
