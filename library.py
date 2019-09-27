#!/usr/bin/python
import json
import os
import re
import zipfile
from config import Config
config = Config()


class Catalogue:
    """Decodes and stores book information"""
    """Step One: filter_books"""
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

    def scan_book(self, book):
        _epub = zipfile.ZipFile(book)
        with _epub as _epub_open:
            try: _epub_open.open('content.opf'); return True
            except Exception as e: print(e); return False

    def filter_books(self, ret=0):
        """
        filter_books(0) -> Catalogue.books
        filter_books(1) -> self.books[]
        :param ret: 0 -> create class property
        :param ret: 1 -> create & return class property
        """
        self.scan_folder()
        regx = re.compile(r"\.epub")
        self.books = list(filter(regx.search, filter(None, self.file_list)))
        _book_list_expanded = {}
        if ret == 0:
            with open(config.book_shelf, 'w') as f:
                for book in self.books:
                    _book_list_expanded[book] = self.process_book(book)
                json.dump(_book_list_expanded, f)
        else:
            return self.books

    def process_book(self, book):
        f_name = 'content.opf'
        book = zipfile.ZipFile(book, 'r')
        details = {}
        with book as book_zip:
            details['files'] = []
            expanded = book_zip.infolist()
            regx = re.compile(r'\.opf|cover')
            for i in expanded:
                match = re.search(regx, i.filename)
                if match:
                    # Returns zip file location of requested files
                    details['files'].append(match.string)
        return details

    def compare_shelf_current(self):
        try:
            self.books
        except Exception:
            self.filter_books()
        unique = set(self.books) - set(self.catalogue)
        return unique