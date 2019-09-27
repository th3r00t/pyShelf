#!/usr/bin/python
# import zipfile as Zip
from pyShelf import InitFiles
from config import Config
from library import Catalogue

config = Config()

InitFiles(config.file_array)
Catalogue = Catalogue()
book_list = Catalogue.filter_books(1)
