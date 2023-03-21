"""Pyshelf's Main Storage Class."""
import re
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from pathlib import Path

from .models import Book, Collection


class Storage:
    """Create a new Storage object.

    >>> db = Storage(config)

    Parameters
    ----------
    config : Config()
        Main program configuration.

    Attributes
    ----------
    config : Stores configuration
    sql : Database Name
    user : Database User Name
    password : Database Password
    db_host : Database Host
    db_port : Database Port
    engine : sqlalchemy.create_engine(url, executor, kw)
    """

    def __init__(self, config):
        """Initialize storage object."""
        self.config = config
        self.sql = self.config.catalogue_db
        self.user = self.config.user
        self.password = self.config.password
        self.db_host = self.config.db_host
        self.db_port = self.config.db_port
        self.engine = create_engine(self.get_connection_string(),
                                    pool_pre_ping=True)

    def get_connection_string(self):
        """Get connection string.

        Engine type references config.json:DB_ENGINE.

        Returns
        -------
        str : sqlalchemy Connection String
        """
        if self.config.db_engine == "sqlite":
            return f"sqlite:////{self.config.root}/pyshelf.sqlite3"
        elif self.config.db_engine == "psql":
            return f"postgresql://{self.user}:{self.password}\
                    @{self.db_host}:{self.db_port}/{self.sql}"
        elif self.config.db_engine == "mysql":
            return f"mysql://{self.user}:{self.password}\
                    @{self.db_host}:{self.db_port}/{self.sql}"

    def create_tables(self):
        """Create table structure."""
        tables = [Book, Collection]
        for table in tables:
            table.metadata.create_all(self.engine)

    def insert_book(self, book):
        """Insert a new book into the database.

        Parameters
        ----------
        book: dict()
            Book object to insert.

        Returns
        -------
        bool
            True on success False on failure
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
                    pass
                collections = self.parse_collections_from_path(book)
                _book = Book(
                        title=book[0],
                        author=book[1],
                        cover=cover_image,
                        file_name=book[3],
                        description=book[4],
                        identifier=book[5],
                        publisher=book[6],
                        rights=book[8],
                        tags=book[9],
                        )
                session.add(_book)
                session.commit()
                session.close()
                self.config.logger.info(book[0][0:80])
                return True
            except Exception as e:
                self.config.logger.error(f"{book[0][0:80]} :: {e}")
                return False

    def book_paths_list(self):
        """Get file paths from database for comparison to system files.

        Returns
        -------
        _result : ScalarResult Object
        """
        session = Session(self.engine)
        _result = session.scalars(select(Book.file_name)).fetchall()
        session.close()
        return _result

    def parse_collections_from_path(self, book: dict()) -> list():
        """Parse book path's to determine common folder structure.

        Stores collections based on shared paths.

        Parameters
        ----------
        book : dict()
            Book object to parse.

        Returns
        -------
        collections : list()
            List of collections.
        """
        collections = []
        title_regx = re.compile(r"^[0-9][0-9]*|-|\ \B")
        book_path: Path = Path(book[3])
        store_path: Path = Path(self.config.book_path)
        relative_book_path: Path = book_path.relative_to(store_path)
        for path in relative_book_path.parts:
            collections.append(re.sub(title_regx, "", path).strip())
        collections.pop(-1)
        return collections

    def make_collections(self):
        """Parse book path's to determine common folder structure.

        Stores collections based on shared paths.
        """
        # TODO: Check this still works with the switch to sqlalchemy
        self.config.logger.info("Making collections.")
        _title_regx = re.compile(r"^[0-9][0-9]*|-|\ \B")
        session = Session(self.engine)
        _set = session.execute(select(Book.id, Book.file_name)).all()
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
                    _q = _sess.execute(
                            select(Collection.id).where(
                                Collection.collection == _s,
                                Collection.book_id == book.id,
                                )
                            )
                    _sess.close()
                    if _q.fetchone() is None:
                        _collection = Collection(collection=_s, book_id=book.id)
                        with Session(self.engine) as _sess:
                            try:
                                _sess.add(_collection)
                                _sess.commit()
                                _sess.close()
                                self.config.logger.info(f"Collection {_s} added.")
                            except Exception as e:
                                self.config.logger.error(f"Collection {_s} failed: {e}")
                    _collections.append(_p)
        self.config.logger.info("Finished making collections.")

    def get_books(self, collection=None, skip=None, limit=None):
        """Get books from database.

        Parameters
        ----------
        collection : str
            Collection to filter by.

        Returns
        -------
        _result : ScalarResult Object
        """
        session = Session(self.engine)
        if collection:
            _result = session.execute(
                    select(Book)
                    .join(Collection)
                    .where(Collection.id == collection)
                    .offset(skip)
                    .limit(limit)
                    ).all()
        else:
            _result = session.execute(select(Book).offset(skip).limit(limit)).all()
        session.close()
        return _result

    def get_book(self, id):
        """Get book from database.

        Parameters
        ----------
        id : int
            Book ID to filter by.

        Returns
        -------
        _result : ScalarResult Object
        """
        session = Session(self.engine)
        _result = session.execute(select(Book).where(Book.id == id)).first()
        session.close()
        return _result

    def get_collections(self):
        """Get collections from database.

        Returns
        -------
        _result : ScalarResult Object
        """
        session = Session(self.engine)
        _result = session.execute(select(Collection).join(Book)).all()
        session.close()
        return _result
