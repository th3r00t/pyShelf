#!/usr/bin/python
import datetime
import re
from .models import Book, Collection
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session


class Storage:
    """Contains all methods for system storage"""

    def __init__(self, config):
        self.sql = config.catalogue_db
        self.user = config.user
        self.password = config.password
        self.db_host = config.db_host
        self.db_port = config.db_port
        self.engine = create_engine(f"postgresql://{self.user}:{self.password}@{self.db_host}:{self.db_port}/{self.sql}")
        self.config = config

    def create_tables(self):
        tables = [Book, Collection]
        for table in tables:
            table.metadata.create_all(self.engine)

    def insert_book(self, book):
        """
        Insert book in database
        :returns: True if succeeds False if not
        """
        with Session(self.engine) as session:
            try:
                try:
                    cover_image = book[2].data
                except Exception:
                    cover_image = book[2]
                if not book[2]:  # If cover image is missing unset entry
                    cover_image = None
                if not book[1]:
                    author = "None"
                _book = Book(
                    title=book[0],
                    author=book[1],
                    cover=cover_image,
                    file_name=book[3],
                    description=book[4],
                    identifier=book[5],
                    publisher=book[6],
                    rights=book[8],
                    tags=book[9]
                )
                session.add(_book)
                session.commit()
                session.close()
                self.config.logger.info(book[0][0:80])
                return True
            except Exception as e:
                self.config.logger.error(f"{book[0][0:80]} :: {e}")

    def book_paths_list(self):
        """
        Get file paths from database for comparison to system files
        """
        session = Session(self.engine)
        _result = session.scalars(select(Book.file_name)).fetchall()
        session.close()
        return _result

    def make_collections(self):
        # TODO: Check this still works with the switch to sqlalchemy
        _title_regx = re.compile(r"^[0-9][0-9]*|-|\ \B")
        session = Session(self.engine)
        _set = session.execute(select(Book.book_id, Book.file_name)).all()
        if _set.__len__() > 0:
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
                    _sess = Session(self.engine)
                    _q = _sess.execute(select(Collection.collection_id).where(Collection.collection == _s, Collection.book_id == book.book_id))
                    _sess.close()
                    if _q.fetchone() is None:
                        _collection = Collection(collection=_s, book_id=book.book_id)
                        with Session(self.engine) as _sess:
                            try:
                                _sess.add(_collection)
                                _sess.commit()
                                _sess.close()
                                self.config.logger.info(f"Collection {_s} added.")
                            except Exception as e:
                                self.config.logger.error(f"Collection {_s} failed: {e}")
                    _collections.append(_p)
