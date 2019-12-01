#!/usr/bin/python
import os
import time

from .config import Config
from .storage import Storage

# config = Config()
# Storage = Storage()


class InitFiles:
    """First run file creation operations"""

    def __init__(self, file_array):
        print("Checking for program files")
        for _pointer in file_array:
            time.sleep(1)
            if not os.path.isfile(_pointer):
                self.CreateFile(_pointer)
                print("%s created" % _pointer)
            else:
                print("%s present" % _pointer)
        time.sleep(1)
        print("File check complete.")

    def CreateFile(self, _pointer):
        """
        Checks if file exists and creates it if not
        """
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
        ## TODO Remove me
        Goto next book page
        :return: new current_page
        """
        self.current_page += 1
        return self.current_page

    def previousPage(self):
        """
        ## TODO Remove me
        Goto previous book page
        :return: new current_page
        """
        self.current_page -= 1
        return self.current_page

    def booksPerPage(self, screen_size):
        """
        ## TODO Remove me
        Set books per page
        :param screen_size: Array containing x,y pixel sizes
        :return: self.books_per_page
        """
        x = (self.thumbnail_size[0] * self.thumbnail_scale) + 10
        y = (self.thumbnail_size[1] * self.thumbnail_scale) + 10
        self.books_per_page = int(self.screen_size[0] // x) * int(
            self.screen_size[1] // y
        )
