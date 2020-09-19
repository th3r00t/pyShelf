#!/usr/bin/env python
import os
import sys
import time

from .lib.config import Config
from .lib.library import Catalogue
from .lib.pyShelf import InitFiles
from .lib.storage import Storage

sys.path.append(os.path.abspath("."))


def MakeCollections(root, **kwargs):
    _t1 = time.time()
    try: config = kwargs['config']
    except KeyError as e: config = Config(root)
    # InitFiles(config.file_array)  # Initialize file system
    _storage = Storage(config)
    _storage.make_collections()
    _t2 = time.time()
    scan_time = round(_t2 - _t1)
    config.logger.info("Collections made in {}".format(scan_time))
