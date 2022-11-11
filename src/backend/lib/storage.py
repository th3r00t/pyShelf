#!/usr/bin/python
import datetime
import re

import psycopg2


class Storage:
    """Contains all methods for system storage"""
    def __init__(self, config):
        self.sql = config["DATABASE"]
        self.user = config["USER"]
        self.password = config["PASSWORD"]
        self.db_host = config["DB_HOST"]
        self.db_port = config["DB_PORT"]
        self.db = psycopg2.connect(database=self.sql,
                                   user=self.user,
                                   password=self.password,
                                   host=self.db_host)
        self.config = config
        self.cursor = self.db.cursor()

    def check_ownership(self, table=None):
        if table is None:
            table = "books"
        _q = "SELECT * FROM books"
        try:
            self.cursor.execute(_q)
        except Exception as e:
            if e.pgcode == "42501":
                _q = """ALTER TABLE public.books OWNER to pyshelf;"""
                self.close()
                set_perms = Storage(self.config)
                try:
                    set_perms.cursor.execute(_q)
                    set_perms.close()
                except Exception as e:
                    self.config.logger.error(e)
                    set_perms.close()

    def create_tables(self):
        """Create table structure"""
        q_check = "SELECT * FROM books"
        q_create = """CREATE TABLE books(title text, author text,
        categories text null, cover blob null, pages int null, progress int null,
        file_name text)"""
        try:
            self.cursor.execute(q_check)
        except psycopg2.errors.UndefinedTable:
            self.cursor.execute(q_create)

    def insert_book(self, book):
        """
        Insert book in database
        :returns: True if succeeds False if not
        """
        q = "INSERT INTO books (title, author, cover, progress, file_name, pages, description, identifier, publisher, date, rights, tags) values (%s, %s, %s, 0, %s, 0, %s, %s, %s, %s, %s, %s);"
        try:
            try:
                cover_image = book[2].data
            except:
                cover_image = book[2]
            if not book[2]:  # If cover image is missing unset entry
                cover_image = None
            self.cursor.execute(
                q,
                (
                    book[0],  # title
                    book[1],  # author
                    cover_image,
                    book[3],  # file
                    book[4],  # descr
                    book[5],  # ident
                    book[6],  # publisher
                    datetime.datetime.now(),
                    book[8],  # rights
                    book[9],  # tags
                ),
            )
            self.config.logger.info(book[0][0:80])
            return True
        except Exception as e:
            if e.pgcode == '22007':  # psycopg2's error code for invalid date
                book[7] = psycopg2.Date(int(book[7]), 1, 1)
                self.insert_book(book)
            raise e

    def book_paths_list(self):
        """
        Get file paths from database for comparison to system files
        """
        q = "SELECT file_name FROM books;"
        self.cursor.execute(q)
        try:
            x = self.cursor.fetchall()
        except psycopg2.Error as e:
            self.config.logger.error(e)
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

    def make_collections(self):
        _title_regx = re.compile(r"^[0-9][0-9]*|-|\ \B")
        _q = "SELECT id,file_name FROM books"
        self.cursor.execute(_q)
        _set = self.cursor.fetchall()
        for book in _set:
            path = self.config.book_path + "/"
            _collections = []
            _pathing = book[1].split(path)[1].split("/")
            try:
                _pathing.pop(0)
                _pathing.pop(-1)
            except IndexError:
                continue
            for _p in _pathing:
                _s = _p.replace("'", "")
                _x = re.sub(_title_regx, "", _s)
                _s = _x.strip()
                _q_x = """
                SELECT id FROM collections where collection='%s'\
                AND book_id_id=%s
                """ % (
                    _s,
                    book[0],
                )
                try:
                    self.cursor.execute(_q_x)
                    if len(self.cursor.fetchall()) < 1:
                        self.cursor.execute("""INSERT INTO collections\
                            (collection, book_id_id) VALUES ('%s',%s)""" %
                                            (_s, book[0]))
                        self.config.logger.info(
                            "Collection {} Added".format(_s))
                except Exception as e:
                    self.config.logger.error(e)
                _collections.append(_p)
        self.db.commit()
        self.close()
