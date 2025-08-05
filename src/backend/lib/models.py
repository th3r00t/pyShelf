from typing import Optional
from typing_extensions import Annotated

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]


class Base(DeclarativeBase):
    """Base class for all models."""

from sqlalchemy.orm import relationship

class Book(Base):
    """Book model."""

    __tablename__ = "Book"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
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

    # One book → many collection entries
    collections = relationship("Collection", back_populates="book", cascade="all, delete-orphan")


class Collection(Base):
    """Collection model."""

    __tablename__ = "Collection"

    id: Mapped[int] = mapped_column(primary_key=True)
    collection: Mapped[str]
    book_id: Mapped[int] = mapped_column(ForeignKey("Book.id"))

    # Each collection entry points to one book
    book = relationship("Book", back_populates="collections")