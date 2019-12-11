#!/usr/bin/python
import sqlite3

import psycopg2

from .config import Config

# db_pointer = Config().catalogue_db


class Storage:
    """Contains all methods for system storage"""

    def __init__(self, db_pointer, config):
        # self.db_file = db_pointer
        self.sql = config.catalogue_db
        self.user = config.user
        self.password = config.password
        self.database()
        # self.create_tables()

    def database(self):
        """Create database cursor"""
        try:
            # self.db = sqlite3.connect(self.db_file)
            self.db = psycopg2.connect(database=self.sql, user=self.user)
            self.cursor = self.db.cursor()
            return True
        except Exception as e:
            print(self.sql)
            print(e)
            return False

    def create_tables(self):
        """Create table structure"""
        q_check = "SELECT * FROM books"
        q_create = """CREATE TABLE books(title text, author text,
        categories text null, cover blob null, pages int null, progress int null,
        file_name text)"""
        try:
            self.cursor.execute(q_check)
        except Exception as e:
            self.cursor.execute(q_create)

    def insert_book(self, book):
        """
        Insert book in database
        :returns: True if succeeds False if not
        """
        q_x = (
            "SELECT title FROM books WHERE EXISTS(SELECT * from books WHERE title = %s)"
        )
        q = "INSERT INTO books (title, author, cover, progress, file_name, pages) values (%s, %s, %s, 0, %s, 0)"
        try:
            try:
                cover_image = book[2].data
            except:
                cover_image = book[2]
            x = self.cursor.execute(q_x, (book[0],))
            try:
                len(x.fetchone()) > 0
            except Exception:
                if not book[2]:  # If cover image is missing unset entry
                    cover_image = None
                self.cursor.execute(q, (book[0], book[1], cover_image, book[3]))
            return True
        except Exception as e:
            print(e)
            return False

    def book_paths_list(self):
        """
        Get file paths from database for comparison to system files
        """
        q = """SELECT file_name FROM books"""
        x = self.cursor.execute(q)
        try:
            x = x.fetchall()
        except Exception:
            x = []
        return x

    def commit(self):
        """
        Commit database transactions
        """
        try:
            self.db.commit()
            return True
        except Exception as e:
            return e

    def close(self):
        """
        Close database connection
        """
        self.db.close()
        return True
