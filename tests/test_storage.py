import unittest
import sys
sys.path.insert(1, 'lib/')
from storage import Storage

storage = Storage()

class StorageTest(unittest.TestCase):

    def test_Storage_databasee(self):
        self.assertTrue(storage.database())

    def test_Storage_create_tables(self):
        self.assertIsNot(storage.create_tables(), Exception)
if __name__ == '__main__':
    unittest.main()