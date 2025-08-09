"""Pyshelf's Configuration Object."""
import json
from pathlib import Path, PurePath
import os
from loguru import logger


class Config:
    """Main System Configuration.

    >>> config = Config(root)

    Parameters
    ----------
    root : File system root of program

    Attributes
    ----------
    root : str() stores root.
    config_structure : dict() Default Configuration Structure.
    _fp : str() file pointer to main configuration.
    _cp : Path() object of configuration file.
    _data : dict() parsed json of _fp.
    logger : holds logging configuration from get_logger().
    book_path : directory pointer to main books folder.
    TITLE : str() Program title.
    VERSION : str() Program  version.
    TITLE : str() Combines TITLE & VERSION.
    book_shelf : Deprecation TODO: Is this still in use?
    catalogue_db : str() Database Name.
    user : str() Database user name.
    password : str() Database password.
    db_host : str() Database host.
    db_port : int() Database port.
    file_array : list() copy of book_shelf TODO: See book_shelf
    auto_scan: bool() Do we auto scan on launch?
    allowed_hosts : list() Allowed host list.
    db_engine : str() Desired database engine type.
    db_user : str() Database user name. Duplication Warning.
    db_pass : str() Database password. Duplication Warning.
    build_mode : str() Production | Development mode.

    Methods
    -------
    get_logger : Setup loguru.
    open_file : Parse configuration file.
    """

    def __init__(self, root):
        """Initialize main configuration options."""
        self.root = root
        self.config_structure = {
            "TITLE": "pyShelf E-Book Server",
            "VERSION": "0.7.0",
            "BOOKPATH": "/mnt/books",
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_ENGINE": "sqlite",
            "DATABASE": "pyshelf",
            "USER": "pyshelf",
            "PASSWORD": "pyshelf",
            "BOOKSHELF": "data/shelf.json",
            "ALLOWED_HOSTS": [
                "localhost",
                "127.0.0.1",
                "[::1]",
                "0.0.0.0"
            ],
            "BUILD_MODE": "development"
        }
        env = os.environ.copy()
        self._fp = "config.json"
        try:
            self._cp = Path.joinpath(root, self._fp)
        except AttributeError:
            self._cp = Path(root, self._fp)
        self._data = self.init_config()
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

    def init_config(self):
        try:
            return self.open_file()
        except FileNotFoundError:
            with open(self._fp, 'w') as _config_file:
                json.dump(self.config_structure, _config_file)
                _config_file.close()
            return self.open_file()

    def get_logger(self):
        """Instantiate logging system."""
        _logger = logger
        _logger.add(PurePath(self.root, 'data', 'pyshelf.log'),
                    rotation="2 MB",
                    enqueue=True,
                    colorize=True)
        return _logger

    def open_file(self):
        """Open config.json and reads in configuration options."""
        with open(str(self._cp), "r") as read_file:
            data = json.load(read_file)
        return data
