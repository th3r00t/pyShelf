#!/usr/bin/python
import os
import sys

from lib.config import Config
from lib.library import Catalogue
from lib.pyShelf import InitFiles

ROOT_DIR = os.path.abspath("../..")
sys.path.append(ROOT_DIR)
config = Config(ROOT_DIR)  # Get configuration settings
InitFiles(config.file_array)  # Initialize file system
Catalogue = Catalogue(config)  # Open the Catalogue
Catalogue.import_books()  # Filter Your books
