#!/usr/bin/python
# import zipfile as Zip
import sys
from PIL import Image
sys.path.insert(1, 'lib/')
from pyShelf import InitFiles, Epub
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
Epub().import_books()