#!/usr/bin/python
import json
import os
import re
from config import Config
config = Config()


class Catalogue:
    """Decodes and stores book information"""
    def __init__(self):
        with open(config.book_shelf, 'r') as f:
            try:
                self.catalogue = json.load(f)
                self.current_files = self.scan_folder()
            except Exception:
                with open(config.book_shelf, 'w') as f:
                    json.dump(self.filter_books(), f)

    def scan_folder(self):
        file_list = []
        for f in os.listdir(config.book_path):
            file_list.append(f)
        return file_list

    def filter_books(self):
        scan = self.scan_folder()
        breakpoint()
        regx = re.compile(r"\.epub")
        self.books = list(filter(regx.search, scan))
        return self.books

    def compare_shelf_current(self):
        try:
            self.books
        except Exception:
            self.filter_books()
        breakpoint()
        unique = set(self.books) - set(self.catalogue)
        return unique
