#!/usr/bin/python
import json
import os
import re
from config import Config
config = Config()


class Catalogue:
    """Decodes and stores book information"""
    def __init__(self):
        self.file_list = []
        with open(config.book_shelf, 'r') as f:
            try:
                self.catalogue = json.load(f)
                self.current_files = self.scan_folder()
            except Exception:
                self.filter_books()

    def scan_folder(self, folder=config.book_path):
        for f in os.listdir(folder):
            _path = os.path.abspath(folder+'/'+f)
            #_path = os.path.abspath('.')+'/'+folder+f+'/'
            _is_dir = os.path.isdir(_path.strip()+'/')
            if _is_dir:
                self.file_list.append(self.scan_folder(_path))
            self.file_list.append(_path)

    def filter_books(self, ret=0):
        self.scan_folder()
        regx = re.compile(r"\.epub")
        self.books = list(filter(regx.search, filter(None, self.file_list)))
        if ret == 0:
            with open(config.book_shelf, 'w') as f:
                    json.dump(self.books, f)
        else:
            return self.books

    def compare_shelf_current(self):
        try:
            self.books
        except Exception:
            self.filter_books()
        unique = set(self.books) - set(self.catalogue)
        return unique
