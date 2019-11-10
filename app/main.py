#!/usr/bin/python
import sys

from config import Config
from lib.display import Frontend
from lib.library import Catalogue
from lib.pyShelf import BookDisplay, BookServer, InitFiles

# sys.path.insert(1, 'lib/')

config = Config()  # Get configuration settings
InitFiles(config.file_array)  # Initialize file system
Catalogue = Catalogue()  # Open the Catalogue
UI = Frontend()
Server = BookServer()
# new_books = Catalogue.new_files()
Catalogue.import_books()  # Filter Your books
# Server.run()
# TODO Figure out a system to get books page count
# TODO Update Documentation
# TODO Requirements.txt
