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
        self.create_tables()

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
        categories text, cover blob, pages int, progress int,
        file_name text)'''
        try:
            self.cursor.execute(q_check)
        except sqlite3.OperationalError as e:
            self.cursor.execute(q_create)

    def insert_book(self, book):
        """
        Insert book in database
        :returns: True if succeeds False if not
        """
        q_x = '''SELECT title FROM books WHERE EXISTS(SELECT * from books WHERE `title` = ?)'''
        q = '''INSERT INTO books (title, author, cover, file_name) values (?, ?, ?, ?)'''
        try:
            try: cover_image = book[2].data
            except: cover_image = book[2]
            x = self.cursor.execute(q_x, (book[0],))
            try: len(x.fetchone()) > 0
            except Exception: self.cursor.execute(q, (book[0], book[1], cover_image, book[3]))
            return True
        except Exception as e:
            print(e)
            return False

    def commit(self):
        try: self.db.commit(); return True
        except Exception as e: return False