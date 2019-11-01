import unittest
# sys.path.insert(1, '../')
from lib.library import Catalogue
Catalogue = Catalogue()


class LibraryTest(unittest.TestCase):

    def test_libray_catalogue(self):
        self.assertIsNotNone(Catalogue)

    def test_library_catalogue_filter_books(self):
        self.assertIsNotNone(Catalogue.filter_books())

    def test_library_catalogue_new_files(self):
        self.assertIsNot(Catalogue.new_files(), False)


if __name__ == '__main__':
    unittest.main()
