"""Pyshelf's Main Storage Class."""
import re
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from pathlib import Path

from .models import Book, Collection, BookCollection


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
                # collections = self.parse_collections_from_path(book)
                # breakpoint()
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
                # self.config.logger.info(book[0][0:80])
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
        # collections = []
        # title_regx = re.compile(r"^[0-9][0-9]*|-|\ \B")
        # book_path: Path = Path(book[3])
        # store_path: Path = Path(self.config.book_path)
        # relative_book_path: Path = book_path.relative_to(store_path)
        # for path in relative_book_path.parts:
        #     collections.append(re.sub(title_regx, "", path).strip())
        # collections.pop(-1)
        # return collections
        collections = []
        title_regx = re.compile(r"^[0-9][0-9]*|-|\ \B")
        book_path: Path = Path(book[3])
        store_path: Path = Path(self.config.book_path)
        relative_book_path: Path = book_path.relative_to(store_path)
        # Keep all folder names except the actual file
        for folder in relative_book_path.parts[:-1]:
            clean_name = re.sub(title_regx, "", folder).strip()
            if clean_name:
                collections.append(clean_name)
        return collections

    def make_collections(self):
        """Ensure collections exist and link them to books (many-to-many)."""
        self.config.logger.info("Making collections.")
        session = Session(self.engine)

        # get all books and paths
        books = session.execute(select(Book.id, Book.file_name)).all()
        
        for book_id, file_name in books:
            try:
                relative_parts = Path(file_name).relative_to(self.config.book_path).parts
            except ValueError:
                continue  # skip books outside the configured path

            # exclude the actual file name
            folder = relative_parts[1]
            # for folder in folders:
            #     clean_name = re.sub(r"^[0-9][0-9]*|-|\ \B", "", folder).strip()
            #     if not clean_name:
            #         continue

                # check if collection exists
            collection = session.execute(
                select(Collection).where(Collection.name == folder)
            ).scalar_one_or_none()
            if not collection:
                collection = Collection(name=folder)
                session.add(collection)
                session.flush()  # ensures collection.id is available

            # check link
            link_exists = session.execute(
                select(BookCollection).where(
                    BookCollection.book_id == book_id,
                    BookCollection.collection_id == collection.id
                )
            ).first()

            if not link_exists:
                session.add(BookCollection(book_id=book_id, collection_id=collection.id))

        session.commit()
        session.close()
        self.config.logger.info("Finished making collections.")



    # def get_books(self, collection=None, skip=None, limit=None):
    #     """Get books from database.
    #
    #     Parameters
    #     ----------
    #     collection : str
    #         Collection to filter by.
    #
    #     Returns
    #     -------
    #     _result : ScalarResult Object
    #     """
    #     session = Session(self.engine)
    #     if collection:
    #         _result = session.execute(
    #                 select(Book)
    #                 .join(Collection)
    #                 # .where(Collection.id == collection)
    #                 .where(Collection.name == collection)
    #                 .offset(skip)
    #                 .limit(limit)
    #                 ).all()
    #     else:
    #         _result = session.execute(select(Book).offset(skip).limit(limit)).all()
    #     session.close()
    #     return _result


    def get_books(self, collection=None, skip=None, limit=None):
        """Get books from database.

        Parameters
        ----------
        collection : int or None
            Collection ID to filter by.
        skip : int or None
            Number of records to skip (offset).
        limit : int or None
            Maximum number of records to return.
        """
        with Session(self.engine) as session:
            if collection is not None:
                # Join through BookCollection to filter books in a collection
                result = session.execute(
                    select(Book)
                    .join(BookCollection)
                    .where(BookCollection.collection_id == collection)
                    .offset(skip or 0)
                    # .limit(limit or 100)
                    .limit(limit)
                ).scalars().all()
            else:
                result = session.execute(
                    select(Book)
                    .offset(skip or 0)
                    # .limit(limit or 100)
                    .limit(limit)
                ).scalars().all()
        return result


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
        with Session(self.engine) as session:
            result = session.execute(
                select(Collection).join(BookCollection).distinct()
            ).scalars().all()
        return result
        # session = Session(self.engine)
        # _result = session.execute(select(Collection).join(Book)).all()
        # session.close()
        # return _result
    
    def get_collection(self, name):
        """Get collection from database.

        Returns
        -------
        _result : ScalarResult Object
        """
        session = Session(self.engine)
        _result = session.execute(select(Collection).where(Collection.name == name).join(Book)).all()
        session.close()
        return _result
