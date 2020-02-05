#!/usr/bin/python
import os
import sys
import time

from .lib.config import Config
from .lib.library import Catalogue
from .lib.pyShelf import InitFiles
from .lib.storage import Storage

sys.path.append(os.path.abspath("."))


def execute_scan(root):
    """
    Main scan execution
    :param root: Project root. Required to properly execute program. Sends to configuration.
    """
    _t1 = time.time()
    config = Config(root)  # Get configuration settings
    InitFiles(config.file_array)  # Initialize file system
    Storage(config).check_ownership()
    catalogue = Catalogue(config)  # Open the Catalogue
    catalogue.import_books()
    _t2 = time.time()
    scan_time = round(_t2 - _t1)
    print("Scan Completed.")
    print("Scan Time %s seconds" % scan_time)
