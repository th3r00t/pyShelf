import json
import os
import sys


class Config:
    """
    Main System Configuration
    """
    _fp = "config.json"
    print(os.path)

    def __init__(self, root=os.path.abspath('../')):
        _data = self.open_file(root)
        self.book_path = _data['BOOKPATH']
        self.TITLE = _data['TITLE']
        self.VERSION = _data['VERSION']
        self.TITLE = self.TITLE + " ver " + self.VERSION
        self.book_shelf = _data['BOOKSHELF']
        # self.catalogue_db = "data/catalogue.db"
        self.catalogue_db = root+'/'+_data['DATABASE']
        self.file_array = [
            self.book_shelf,
            self.catalogue_db,
            ]
        self.auto_scan = True

    def open_file(self, root):
        with open(root+'/'+self._fp, "r") as read_file:
            data = json.load(read_file)
        return data
