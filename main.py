#!/usr/bin/python
import sys

from config import Config
from lib.library import Catalogue
from lib.pyShelf import InitFiles

sys.path.insert(1, 'lib/')

config = Config()  # Get configuration settings
InitFiles(config.file_array)  # Initialize file system
Catalogue = Catalogue()  # Open the Catalogue

# new_books = Catalogue.new_files()
Catalogue.import_books()  # Filter Your books
# TODO Figure out a system to get books page count
# TODO Update Documentation
# TODO Requirements.txt
