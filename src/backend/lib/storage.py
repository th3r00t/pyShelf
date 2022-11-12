#!/usr/bin/python
import datetime
import re
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


class Storage:
    """Contains all methods for system storage"""

    def __init__(self, config):
        self.sql = config["DATABASE"]
        self.user = config["USER"]
        self.password = config["PASSWORD"]
        self.db_host = config["DB_HOST"]
        self.db_port = config["DB_PORT"]
        self.db = create_engine(f"postgresql://{self.user}:{self.password}@{self.db_host}:{self.db_port}/{self.sql}")
        self.config = config

    def check_ownership(self, table=None):
        if table is None:
            table = "books"
        _q = "SELECT * FROM books"
        try:
            self.transact(_q)
        except Exception as e:
            if e.pgcode == "42501":
                _q = """ALTER TABLE public.books OWNER to pyshelf;"""
                try:
                    self.transact(_q)
                except Exception as e:
                    self.config.logger.error(e)

    def transact(self, query):
        try:
            with Session(self.db.connect()) as _sess:
                try:
                    _sess.execute(text(query))
                    _sess.commit()
                except Exception:
                    # TODO: Raise Exception
                    pass
            _sess.close()
            return True
        except Exception:
            return False

    def create_tables(self):
        """Create table structure"""
        tables = [
            "CREATE TABLE books(title text, author text, categories text null,\
            cover bytea null, pages int null, progress int null,\
            file_name text, book_id int NOT NULL UNIQUE PRIMARY KEY)",

            "CREATE TABLE collections(collection text, book_id int,\
            CONSTRAINT book_id FOREIGN KEY(book_id) REFERENCES books(book_id),\
            collection_id int NOT NULL UNIQUE PRIMARY KEY)"
        ]
        for table in tables:
            self.transact(table)

    def insert_book(self, book):
        """
        Insert book in database
        :returns: True if succeeds False if not
        """
        q = "INSERT INTO books (title, author, cover, progress, file_name,\
                                pages, description, identifier, publisher,\
                                date, rights, tags) values (%s, %s, %s, 0, %s,\
                                                            0, %s, %s, %s, %s,\
                                                            %s, %s);"
        try:
            try:
                cover_image = book[2].data
            except Exception:
                cover_image = book[2]
            if not book[2]:  # If cover image is missing unset entry
                cover_image = None
            _query = text(q, (
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
            ))
            self.transact(_query)
            self.config.logger.info(book[0][0:80])
            return True
        except Exception as e:
            # TODO: Handle Invalid Date Exception here
            breakpoint()
            if e.pgcode == '22007':  # psycopg2's error code for invalid date
                print(e)
                # book[7] = psycopg2.Date(int(book[7]), 1, 1)
                # self.insert_book(book)
            raise e

    def book_paths_list(self):
        """
        Get file paths from database for comparison to system files
        """
        q = "SELECT file_name FROM books;"
        self.cursor.execute(q)
        try:
            # TODO: Get all rows
            x = self.cursor.fetchall()
        except Exception as e:
            self.config.logger.error(e)
            x = []
        return x

    def make_collections(self):
        # TODO: Check this still works with the switch to sqlalchemy
        _title_regx = re.compile(r"^[0-9][0-9]*|-|\ \B")
        _q = "SELECT id,file_name FROM books"
        self.cursor.execute(_q)
        # TODO: Get all rows
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
                    # TODO: Get all rows
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
