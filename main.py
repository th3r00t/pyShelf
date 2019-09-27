#!/usr/bin/python
# import zipfile as Zip
from pyShelf import InitFiles
from config import Config
from library import Catalogue
# Get configuration settings
config = Config()
# Initialize file system
InitFiles(config.file_array)
# Open the Catalogue
Catalogue = Catalogue()
# Filter Your books
# This only needs to be run on first run, & when new books are added
book_list = Catalogue.filter_books(0)

