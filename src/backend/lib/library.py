#!/usr/bin/env python
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
        self.title_sanitization_regx = re.compile(r"^(Book )+[0-9]*")
        self.title_sanitization_lvl2_regx = re.compile(r"^(Book )+[0-9]*\W+(-)")
        self.root_dir = config.root
        self.book_folder = config.book_path
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
        print(str(book), end='\r', flush=True)
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
            if re.match(self.title_sanitization_regx, title):
                if re.match(self.title_sanitization_lvl2_regx, title):
                    title = re.split(r"-+\W", title)[1]
                else: title = re.split(self.title_sanitization_regx, title)[2]

            author = soup.find("dc:creator")
            if author is not None:
                author = author.contents[0]
            try:
                cover = self.extract_cover_image(f, book)
            except IndexError:
                # cover = self.extract_cover_html(book_zip, book)
                cover = DuckDuckGo().image_result(title)
            try:
                description = self.stripTags(soup.find("dc:description").text)
            except AttributeError:
                description = None
            try:
                identifier = self.stripTags(soup.find("dc:identifier").text)
            except AttributeError:
                identifier = None
            try:
                publisher = self.stripTags(soup.find("dc:publisher").text)
            except AttributeError:
                publisher = None
            try:
                date = self.stripTags(soup.find("dc:date").text)
            except AttributeError:
                date = None
            try:
                rights = self.stripTags(soup.find("dc:rights").text)
            except AttributeError:
                rights = None
            try:
                tags = soup.find_all("dc:subject")
            except AttributeError:
                tags = None
            ftags = None
            if tags is not None:
                for tag in tags:
                    if ftags is None:
                        ftags = tag.text
                    else:
                        ftags = ftags + "," + tag.text
            book_details = [
                title,
                author,
                cover,
                book["path"],
                description,
                identifier,
                publisher,
                date,
                rights,
                ftags,
            ]
        return book_details

    @staticmethod
    def stripTags(source):
        p = re.compile(r"<.*?>")
        return p.sub("", source)

    def extract_metadata_mobi(self, book):
        book = Mobi(book)
        book.parse()
        try:
            cover_image = book.readImageRecord(0)
        except KeyError:
            cover_image = None
        title = book.title().decode("utf-8")
        author = book.author().decode("utf-8")
        book_config = book.config
        try:
            description = self.stripTags(book_config['exth']['records'][103].decode("utf-8"))
        except KeyError:
            description = None
        try:
            identifier = book_config['exth']['records'][104].decode("utf-8")
        except KeyError:
            identifier = None
        try:
            publisher = book_config['exth']['records'][101].decode("utf-8")
        except KeyError:
            publisher = None
        date = None
        rights = None
        try:
            ftags = book_config['exth']['records'][105].decode("utf-8")
            if ":" in ftags:
                ftags = ftags.replace(":", ",")
            elif ";" in ftags:
                ftags = ftags.replace(";", ",")
            # elif re.search(r"\s", ftags):  # Must be final assignment to avoid spliting on multiple delimeters
            #    ftags = ftags.replace(" ", ",")
        except KeyError:
            ftags = None
        return [
            title,
            author,
            cover_image,
            book.f.name,
            description,
            identifier,
            publisher,
            date,
            rights,
            ftags,
        ]

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
        # TODO Refactor metadata extraction into process_book \
        # call to more easily handle additional formats
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
