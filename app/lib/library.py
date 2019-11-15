#!/usr/bin/python
import json
import os
import re
import zipfile

from bs4 import BeautifulSoup
from PIL import Image

from .api_hooks import DuckDuckGo
from .config import Config
from .storage import Storage

# config = Config()


class Catalogue:
    """Decodes and stores book information"""
    """Step One: filter_books"""

    def __init__(self, root):
        self.file_list = []
        self.opf_regx = re.compile(r'\.opf')
        self.cover_regx = re.compile(r'\.jpg|\.jpeg|\.png|\.bmp|\.gif')
        self.html_regx = re.compile(r'\.html')
        self.root_dir = root
        _config = Config(root)
        self.book_folder = _config.book_path
        self.book_shelf = _config.book_shelf
        self._book_list_expanded = None
        self.books = None

    def scan_folder(self, _path=None):
        if _path is not None:
            folder = _path
        elif os.path.isdir(self.root_dir+'/'+self.book_folder):
            folder = self.root_dir+'/'+self.book_folder
        else: folder = self.book_folder
        for f in os.listdir(folder):
            _path = os.path.abspath(folder+'/'+f)
            _is_dir = os.path.isdir(_path.strip()+'/')
            if _is_dir:
                self.file_list.append(self.scan_folder(_path))
            self.file_list.append(_path)

    def filter_books(self):
        """
            Scan book folder recursively for epub files
            filter_books(0) -> Catalogue.books
            filter_books(1) -> self.books[]
            :param ret: 0 -> create class property -> dump json
            :param ret: 1 -> create & return class property
        """
        self.scan_folder()
        regx = re.compile(r"\.epub")
        try:
            self.books = list(filter(regx.search, filter(None, self.file_list)))
        except TypeError as e:
            print(e)
        self._book_list_expanded = {}
        with open(self.book_shelf, 'w') as f:
            for book in self.books:
                self._book_list_expanded[book] = self.process_book(book)
            json.dump(self._book_list_expanded, f)
        return self._book_list_expanded

    @staticmethod
    def process_book(book):
        """Return dictionary of epub file contents"""
        book = zipfile.ZipFile(book, 'r')
        details = {}
        with book as book_zip:
            details['files'] = []
            details['path'] = book.filename
            expanded = book_zip.infolist()
            regx = re.compile(r'\.opf|cover')
            for i in expanded:
                match = re.search(regx, i.filename)
                if match:
                    # Returns zip file location of requested files
                    details['files'].append(match.string)
        return details

    def extract_metadata(self, book):
        """
        Return extracted metadata and cover picture
        book['path'] == Full path to ebook file
        book['files'] == list of files from self.process_book(book)
        """
        book_zip = zipfile.ZipFile(book['path'], 'r')
        with book_zip as f:
            content = self.extract_content(book_zip, book)
            soup = BeautifulSoup(content, "lxml")
            title = soup.find("dc:title")
            if title is None:
                title = book['path'].split('/')[-1].rsplit('.', 1)[0]
            else: title = title.contents[0]
            author = soup.find("dc:creator")
            if author is not None: author = author.contents[0]
            try: cover = self.extract_cover_image(book_zip, book)
            except IndexError:
                # cover = self.extract_cover_html(book_zip, book)
                cover = DuckDuckGo().image_result(title)
            book_details = [title, author, cover, book['path']]
        return book_details

    def extract_content(self, book_zip, book):
        content = book_zip.open(
            list(
                filter(self.opf_regx.search, book['files'])
            )[0]
        )
        return content

    def extract_cover_html(self, book_zip, book):
        cover = book_zip.open(
            list(
                filter(self.html_regx.search, book['files'])
            )[0]
        )
        return cover

    def extract_cover_image(self, book_zip, book):
        cover = book_zip.open(
            list(
                filter(self.cover_regx.search, book['files'])
            )[0]
        )
        try: cover = book_zip.read(cover.name); return cover
        except KeyError: return False

    def compare_shelf_current(self):
        db = Storage()
        stored = db.book_paths_list()
        closed = db.close()
        if self.books is None:
            self.filter_books()
        on_disk, in_storage = [], []
        for _x in self.books: on_disk.append(_x)
        for _y in stored: in_storage.append(_y[0])
        a, b, = set(on_disk), set(in_storage)
        c = set.difference(a, b)
        return c

    def import_books(self, list=None):
        book_list = self.compare_shelf_current()
        db = Storage()
        for book in book_list:
            book = self.process_book(book)
            extracted = self.extract_metadata(book)
            db.insert_book(extracted)
        inserted = db.commit()
        if inserted is not True:
            print(inserted)
            if input('Continue ? y/n') == 'y':
                pass
        db.close()
