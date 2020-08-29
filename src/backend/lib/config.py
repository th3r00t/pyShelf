import json
import pathlib
import re

from loguru import logger


class Config:
    """
    Main System Configuration
    """


    def __init__(self, root):
        """
        Initialize main configuration options
        """
        self.root = root
        self._fp = "config.json"
        self._cp = pathlib.Path.joinpath(root, self._fp)
        self._data = self.open_file()
        self.logger = self.get_logger()
        self.book_path = self._data["BOOKPATH"]
        self.TITLE = self._data["TITLE"]
        self.VERSION = self._data["VERSION"]
        self.TITLE = self.TITLE + " ver " + self.VERSION
        self.book_shelf = self._data["BOOKSHELF"]
        self.catalogue_db = self._data["DATABASE"]
        self.user = self._data["USER"]
        self.password = self._data["PASSWORD"]
        self.db_host = self._data["DB_HOST"]
        self.db_port = self._data["DB_PORT"]
        self.file_array = [
            self.book_shelf,
        ]
        self.auto_scan = True

        self.allowed_hosts = self._data["ALLOWED_HOSTS"]
        self.db_user = self._data["USER"]
        self.db_pass = self._data["PASSWORD"]
        self.SECRET = self._data["SECRET"]

    def get_logger(self):
        _logger = logger
        _logger.add(pathlib.PurePath(self.root, 'data','pyShelf_{time}.log'),
                    rotation="10 MB", enqueue=True, colorize=True)
        return _logger

    def open_file(self):
        """
        Opens config.json and reads in configuration options
        """
        with open(str(self._cp), "r") as read_file:
            data = json.load(read_file)
        return data

    def path(self):
        rstr = "pyShelf/src"
        r = re.template(rstr)
        _pathre = re.match("pyShelf/src")

    def django_secret(self):
        pass
