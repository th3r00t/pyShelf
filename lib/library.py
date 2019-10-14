#!/usr/bin/python
import json
import os
import re
import zipfile
# import sys
# sys.path.insert(1, '../')
from lib.storage import Storage
from bs4 import BeautifulSoup
from config import Config
from lib.api_hooks import DuckDuckGo

config = Config()


class Catalogue:
    """Decodes and stores book information"""
    """Step One: filter_books"""
    def __init__(self):
        self.file_list = []
        self.opf_regx = re.compile(r'\.opf')
        self.cover_regx = re.compile(r'\.jpg|\.jpeg|\.png|\.bmp|\.gif')
        self.html_regx = re.compile(r'\.html')
        self.scan_folder()

    def scan_folder(self, folder=config.book_path):
        for f in os.listdir(folder):
            _path = os.path.abspath(folder + '/' + f)
            # _path = os.path.abspath('.')+'/'+folder+f+'/'
            _is_dir = os.path.isdir(_path.strip() + '/')
            if _is_dir:
                self.file_list.append(self.scan_folder(_path))
            self.file_list.append(_path)
        regx = re.compile(r"\.epub")
        self.books = list(filter(regx.search, filter(None, self.file_list)))

    def scan_book(self, book):
        """REMOVE ME?"""
        _epub = zipfile.ZipFile(book)
        with _epub as _epub_open:
            try:
                _epub_open.open('content.opf')
                return True
            except Exception as e:
                print(e)
                return False

    def filter_books(self, ret=0):
        """
        Scan book folder recursively for epub files
        filter_books(0) -> Catalogue.books
        filter_books(1) -> self.books[]
        :param ret: 0 -> create class property -> dump json
        :param ret: 1 -> create & return class property
        """
        _book_list_expanded = {}
        with open(config.book_shelf, 'w') as f:
            for book in self.books:
                _book_list_expanded[book] = self.process_book(book)
            if ret != 0: return _book_list_expanded
            else:
                json.dump(_book_list_expanded, f)
                return _book_list_expanded

    def process_book(self, book):
        """Return dictionary of epub file contents"""
        f_name = 'content.opf'
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
            if title == None:
                title = book['path'].split('/')[-1].rsplit('.', 1)[0]
            else:
                title = title.contents[0]
            author = soup.find("dc:creator")
            if author != None: author = author.contents[0]
            try:
                cover = self.extract_cover_image(book_zip, book)
            except IndexError:
                # cover = self.extract_cover_html(book_zip, book)
                cover = DuckDuckGo().image_result(title)
            book_details = [title, author, cover, book['path']]
        return book_details

    def extract_content(self, book_zip, book):
        content = book_zip.open(
            list(filter(self.opf_regx.search, book['files']))[0])
        return content

    def extract_cover_html(self, book_zip, book):
        cover = book_zip.open(
            list(filter(self.html_regx.search, book['files']))[0])
        return cover

    def extract_cover_image(self, book_zip, book):
        # TODO Handle books that have no Cover Image
        # TODO Handle books with html covers
        cover = book_zip.open(
            list(filter(self.cover_regx.search, book['files']))[0])
        try:
            cover = book_zip.read(cover.name)
            return cover
        except KeyError:
            return False

    def new_files(self):
        storage = Storage()
        try:
            a = []
            stored = storage.book_paths_list()
            for i in stored: a.append(i[-1])
            unique = set(self.books) - set(a)
            return unique
        except Exception:
            return False
