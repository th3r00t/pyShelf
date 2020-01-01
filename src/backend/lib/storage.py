#!/usr/bin/python
import sqlite3

import psycopg2
from psycopg2 import Error

from .config import Config

# db_pointer = Config().catalogue_db


class Storage:
    """Contains all methods for system storage"""

    def __init__(self, config):
        self.sql = config.catalogue_db
        self.user = config.user
        self.password = config.password
        self.db_host = config.db_host
        self.db_port = config.db_port
        self.db = psycopg2.connect(
            database=self.sql, user=self.user, password=self.password, host=self.db_host
        )
        self.config = config
        self.cursor = self.db.cursor()

    def check_ownership(self, table=None):
        if table is None:
            table = "books"
        _q = "SELECT * FROM books"
        try:
            self.cursor.execute(_q)
        except Exception as e:
            breakpoint()
            if e.pgcode == "42501":
                _q = """ALTER TABLE public.books OWNER to pyshelf;"""
                self.close()
                set_perms = Storage(self.config)
                try:
                    set_perms.cursor.execute(_q)
                    set_perms.close()
                except Exception as e:
                    print(e)
                    set_perms.close()

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
        q = "INSERT INTO books (title, author, cover, progress, file_name, pages) values (%s, %s, %s, 0, %s, 0);"
        try:
            try:
                cover_image = book[2].data
            except:
                cover_image = book[2]
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
        q = "SELECT file_name FROM books;"
        self.cursor.execute(q)
        try:
            x = self.cursor.fetchall()
        except psycopg2.Error as e:
            print(e)
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
