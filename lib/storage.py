#!/usr/bin/python
import sys
import sqlite3
sys.path.insert(1,'../')
from config import Config
db_pointer = Config().catalogue_db


class Storage:
    """Contains all methods for system storage"""

    def __init__(self):
        self.db_file = db_pointer
        self.database()

    def database(self):
        """Create database cursor"""
        try:
            self.db = sqlite3.connect(self.db_file)
            self.cursor = self.db.cursor()
            return True
        except Exception as e:
            return False

    def create_tables(self):
        """Create table structure"""
        q_check = "SELECT * FROM books"
        q_create = '''CREATE TABLE books(title text, author text,
        categories text, cover blob,  pages int, progress int,
        file_name text)'''
        try:
            self.cursor.execute(q_check)
        except Exception as e:
            self.cursor.execute(q_create)

    def insert_book(self, book):
        """
        Insert book in database
        :returns: True if succeeds False if not
        """
        q = '''INSERT INTO books (title, author, categories, cover,
        pages, progress, file_name) values (%s, %s, %s, %s, 0, %s)''' % ()
        try:
            self.cursor.execute(q)
            return True
        except Exception as e:
            print(e)
            return False