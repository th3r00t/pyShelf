import unittest
import os
import shutil
import sys
sys.path.insert(1, 'lib/')
from pyShelf import InitFiles
from pyShelf import Epub


class SysIoTest(unittest.TestCase):

    def test_sysio_InitFiles(self):
        file_array = ["temp/test_file_1", "temp/test_file_2"]
        InitFiles(file_array)
        self.assertTrue(os.path.isfile(file_array[0]))

    def tearDown(self):
        try:
            shutil.rmtree("temp")
        except Exception as e:
            pass

if __name__ == '__main__':
    unittest.main()
