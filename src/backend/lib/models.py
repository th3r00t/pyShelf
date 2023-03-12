from typing import Optional
from typing_extensions import Annotated
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP())
]


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class Book(Base):
    """Book model."""

    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str]
    author: Mapped[Optional[str]]
    categories: Mapped[Optional[str]]
    cover: Mapped[Optional[bytes]]
    pages: Mapped[Optional[int]]
    progress: Mapped[Optional[float]]
    file_name: Mapped[str]
    description: Mapped[Optional[str]]
    date: Mapped[timestamp]
    rights: Mapped[Optional[str]]
    tags: Mapped[Optional[str]]
    identifier: Mapped[Optional[str]]
    publisher: Mapped[Optional[str]]



class Collection(Base):
    """Collection model."""

    __tablename__ = "collections"

    collection: Mapped[str]
    book_id: Mapped[int] = mapped_column(ForeignKey(Book.book_id))
    collection_id: Mapped[int] = mapped_column(primary_key=True)
