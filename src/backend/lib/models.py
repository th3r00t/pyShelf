from typing import Optional
from typing_extensions import Annotated

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

# Timestamp annotation
timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]


class Base(DeclarativeBase):
    """Base class for all models."""


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

    # Relationship to join table
    book_collections = relationship(
        "BookCollection", back_populates="book", cascade="all, delete-orphan"
    )


class Collection(Base):
    """Collection model."""

    __tablename__ = "Collection"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    # Relationship to join table
    book_collections = relationship(
        "BookCollection", back_populates="collection", cascade="all, delete-orphan"
    )


class BookCollection(Base):
    """Association table linking Books and Collections."""

    __tablename__ = "BookCollection"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("Book.id"))
    collection_id: Mapped[int] = mapped_column(ForeignKey("Collection.id"))

    # Relationships
    book = relationship("Book", back_populates="book_collections")
    collection = relationship("Collection", back_populates="book_collections")
