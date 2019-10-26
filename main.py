#!/usr/bin/python
import sys
sys.path.insert(1, 'lib/')
from pyShelf import InitFiles
from config import Config
from library import Catalogue

config = Config()  # Get configuration settings
InitFiles(config.file_array)  # Initialize file system
Catalogue = Catalogue()  # Open the Catalogue
# new_books = Catalogue.new_files()
Catalogue.import_books()  # Filter Your books
# TODO Resolve database locking after querying for book list
# TODO Figure out a system to get books page count
# TODO Update Documentation
# TODO Requirements.txt
