#!/usr/bin/python
import os
import zipfile
from config import Config
from lib.library import Catalogue
from lib.storage import Storage
config = Config()
Storage = Storage()


class InitFiles:
    """First run file creation operations"""
    def __init__(self, file_array):
        print("Begining creation of file structure")
        for _pointer in file_array:
            if not os.path.isfile(_pointer):
                self.CreateFile(_pointer)

    def CreateFile(self, _pointer):
        """Create the file"""
        if not os.path.isdir(os.path.split(_pointer)[0]):
            os.mkdir(os.path.split(_pointer)[0])
            f = open(_pointer, "w+")
        f.close()
