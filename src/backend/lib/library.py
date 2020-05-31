#!/usr/bin/python
import json
import os
import pathlib
import re
import zipfile

from bs4 import BeautifulSoup

from mobi import Mobi

from .api_hooks import DuckDuckGo
from .config import Config
from .storage import Storage

# config = Config()


class Catalogue:
    """
    Decodes book metadata for storage
    """

    def __init__(self, config):
        self.file_list = []
        self.opf_regx = re.compile(r"\.opf")
        self.cover_regx = re.compile(r"\.jpg|\.jpeg|\.png|\.bmp|\.gif")
        self.html_regx = re.compile(r"\.html")
        self.root_dir = config.root
        self.book_folder = config.book_path
        # self.book_shelf = config.book_shelf
        self.books = None
        self.db_pointer = config.catalogue_db
        self.config = config

    def scan_folder(self, _path=None):
        """
        Scan folder by _path, allows recurisive scanning
        """
        if _path is not None:
            folder = _path
        elif os.path.isdir(str(self.root_dir) + "/" + self.book_folder):
            folder = str(self.root_dir) + "/" + self.book_folder
        else:
            folder = self.book_folder
        for f in os.listdir(folder):
            _path = os.path.abspath(folder + "/" + f)
            if os.path.isdir(_path.strip() + "/"):
                self.file_list.append(self.scan_folder(_path))
            else:
                self.file_list.append(_path)

    def filter_books(self):
        """
        Calls scan_folder and filters out book files
        Proceeds to call process_book

        :returns self._book_list_expanded: json string containing all book metadata
        """
        self.scan_folder()  # Populate file list
        regx = re.compile(r"\.epub|\.mobi")
        try:
            self.books = list(filter(regx.search, filter(None, self.file_list)))
        except TypeError as e:
            print(e)
        """
        for book in self.books:
            self._book_list_expanded[book] = self.process_by_filetype(book)
        return self._book_list_expanded
        """

    def process_by_filetype(self, book):
        if book.endswith(".epub"):
            epub = self.process_epub(book)
            return self.extract_metadata_epub(epub)
        elif book.endswith(".mobi"):
            return self.extract_metadata_mobi(book)

    @staticmethod
    def process_epub(book):
        """Return dictionary of epub file contents"""
        details = {}
        book = zipfile.ZipFile(book, "r")
        with book as book_zip:
            details["files"] = []
            details["path"] = book.filename
            expanded = book_zip.infolist()
            regx = re.compile(r"\.opf|cover")
            for i in expanded:
                match = re.search(regx, i.filename)
                if match:
                    # Returns zip file location of requested files
                    details["files"].append(match.string)
        return details

    def extract_metadata_epub(self, book):
        """
        Return extracted metadata and cover picture
        book['path'] == Full path to ebook file
        book['files'] == list of files from self.process_book(book)
        """
        book_zip = zipfile.ZipFile(book["path"], "r")
        with book_zip as f:
            content = self.extract_content(f, book)
            soup = BeautifulSoup(content, "lxml")
            title = soup.find("dc:title")
            if title is None:
                title = book["path"].split("/")[-1].rsplit(".", 1)[0]
            else:
                title = title.contents[0]
            author = soup.find("dc:creator")
            if author is not None:
                author = author.contents[0]
            try:
                cover = self.extract_cover_image(f, book)
            except IndexError:
                # cover = self.extract_cover_html(book_zip, book)
                cover = DuckDuckGo().image_result(title)
            book_details = [title, author, cover, book["path"]]
        return book_details

    @staticmethod
    def extract_metadata_mobi(book):
        book = Mobi(book)
        book.parse()
        try:
            cover_image = book.readImageRecord(0)
        except KeyError:
            cover_image = None
        title = book.title().decode("utf-8")
        author = book.author().decode(
            "utf-8"
        )  # TODO some files are still passing encoded data for author.
        return [title, author, cover_image, book.f.name]

    def extract_content(self, book_zip, book):
        """
        Opens epub as zip file filters then stores as list any files matching opf_regx
        """
        content = book_zip.open(list(filter(self.opf_regx.search, book["files"]))[0])
        return content

    def extract_cover_html(self, book_zip, book):
        """
        Opens epub as zip file filters then stores as list any files matching html_regx
        """
        cover = book_zip.open(list(filter(self.html_regx.search, book["files"]))[0])
        return cover

    def extract_cover_image(self, book_zip, book):
        """
        Opens epub as zip file filters then stores as list any files matching cover_regx
        """
        cover = book_zip.open(list(filter(self.cover_regx.search, book["files"]))[0])
        try:
            cover = book_zip.read(cover.name)
            return cover
        except KeyError:
            return False

    def compare_shelf_current(self):
        """
        Calls storage system, gets list of books stored and compares against files on disk
        """
        db = Storage(self.config)
        stored = db.book_paths_list()
        db.close()
        if self.books is None:
            self.filter_books()
        on_disk, in_storage = [], []
        for _x in self.books:
            on_disk.append(_x)
        for _y in stored:
            in_storage.append(_y[0])
        a, b, = set(on_disk), set(in_storage)
        c = set.difference(a, b)
        return c

    def import_books(self, list=None):
        """
        Main entry point for import operations.
        Gets a list of new files via compare_shelf_current.
        Iterates over list and inserts new books into database.
        """
        # TODO Refactor metadata extraction into process_book call to more easily handle additional formats
        book_list = self.compare_shelf_current()
        db = Storage(self.config)
        for book in book_list:
            book = self.process_by_filetype(book)
            db.insert_book(book)
        inserted = db.commit()
        if inserted is not True:
            print(inserted)
            if input("Continue ? y/n") == "y":
                pass
        db.close()
