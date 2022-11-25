"""Pyshelf's Configuration Object."""
import json
import pathlib
import os
from loguru import logger


class Config:
    """Main System Configuration."""

    def __init__(self, root):
        """Initialize main configuration options."""
        self.root = root
        env = os.environ.copy()
        self._fp = "config.json"
        try:
            self._cp = pathlib.Path.joinpath(root, self._fp)
        except AttributeError:
            self._cp = pathlib.Path(root, self._fp)
        self._data = self.open_file()
        try:
            self.logger
        except AttributeError:
            self.logger = self.get_logger()
        self.book_path = env.get("BOOKPATH", self._data["BOOKPATH"])
        self.TITLE = env.get("TITLE", self._data["TITLE"])
        self.VERSION = env.get("VERSION", self._data["VERSION"])
        self.TITLE = self.TITLE + " ver " + self.VERSION
        self.book_shelf = env.get("BOOKSHELF", self._data["BOOKSHELF"])
        self.catalogue_db = env.get("DATABASE", self._data["DATABASE"])
        self.user = self._data["USER"]
        self.password = self._data["PASSWORD"]
        self.db_host = env.get("DB_HOST", self._data["DB_HOST"])
        self.db_port = env.get("DB_PORT", self._data["DB_PORT"])
        self.file_array = [self.book_shelf]
        self.auto_scan = True
        self.allowed_hosts = env.get("ALLOWED_HOSTS",
                                     self._data["ALLOWED_HOSTS"])
        self.db_engine = env.get("DB_ENGINE", self._data["DB_ENGINE"])
        self.db_user = env.get("USER", self._data["USER"])
        self.db_pass = env.get("PASSWORD", self._data["PASSWORD"])
        self.build_mode = env.get("BUILD_MODE", self._data["BUILD_MODE"])

    def get_logger(self):
        """Instantiate logging system."""
        _logger = logger
        _logger.add(pathlib.PurePath(self.root, 'data', 'pyshelf.log'),
                    rotation="2 MB",
                    enqueue=True,
                    colorize=True)
        return _logger

    def open_file(self):
        """Open config.json and reads in configuration options."""
        with open(str(self._cp), "r") as read_file:
            data = json.load(read_file)
        return data
