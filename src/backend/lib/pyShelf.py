#!/usr/bin/python
import os

from .config import Config
from .storage import Storage

# config = Config()
# Storage = Storage()


class InitFiles:
    """First run file creation operations"""

    def __init__(self, file_array):
        print("Begining creation of file structure")
        for _pointer in file_array:
            if not os.path.isfile(_pointer):
                self.CreateFile(_pointer)
        print("Concluded file creation")

    def CreateFile(self, _pointer):
        """Create the file"""
        if not os.path.isdir(os.path.split(_pointer)[0]):
            os.mkdir(os.path.split(_pointer)[0])
            f = open(_pointer, "w+")
            f.close()


class BookDisplay:
    """All functions related to displaying book information in the HTML UI"""

    def __init__(self, **kwargs):
        """
        Initialize class variables
        :return: None
        """
        self.books_per_page = None
        self.current_page = 0
        self.thumbnail_size = [200, 300]
        self.thumbnail_scale = 1
        self.total_pages = None
        try:
            self.screen_size = kwargs["screen_size"]
        except Exception:
            self.screen_size = [900, 600]

    def nextPage(self):
        """
        Goto next book page
        :return: new current_page
        """
        self.current_page += 1
        return self.current_page

    def previousPage(self):
        """
        Goto previous book page
        :return: new current_page
        """
        self.current_page -= 1
        return self.current_page

    def booksPerPage(self, screen_size):
        """
        Set books per page

        :param screen_size: Array containing x,y pixel sizes
        :return: self.books_per_page
        """
        x = (self.thumbnail_size[0] * self.thumbnail_scale) + 10
        y = (self.thumbnail_size[1] * self.thumbnail_scale) + 10
        self.books_per_page = int(self.screen_size[0] // x) * int(
            self.screen_size[1] // y
        )
