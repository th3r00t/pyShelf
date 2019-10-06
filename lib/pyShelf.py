#!/usr/bin/python
import os
import zipfile
from config import Config
from library import Catalogue
from storage import Storage
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


class Epub:
    """All Epub file handling"""
    def __init__(self):
        global config
        self.book_path = config.book_path
        self.Catalogue = Catalogue()

    def import_books(self):
        book_list = self.Catalogue.filter_books()
        for book in book_list:
            extracted = self.Catalogue.extract_metadata(book_list[book])
            Storage.insert_book(extracted)
        Storage.commit()

    def book_list(self):
        pass
