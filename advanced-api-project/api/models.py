"""
Database models for the API application.

This module defines two simple domain objects: ``Author`` and
``Book``.  An ``Author`` has a single ``name`` field to store the
author’s name.  A ``Book`` has a ``title`` and ``publication_year``
along with a foreign key to its ``Author``.  The relationship is
one‑to‑many: each author can have many books but each book is
associated with exactly one author.

The ``related_name`` on the ``author`` field allows reverse lookups
from an ``Author`` instance to the set of ``Book`` instances via
``author.books.all()``.  This is leveraged in the serializer layer
to provide nested book data when serialising authors.
"""
from django.db import models


class Author(models.Model):
    """Represents an author who has written one or more books.

    Fields
    ------
    name : CharField
        Stores the full name of the author.  A reasonable maximum
        length of 255 characters is imposed to prevent overly long
        values.  This field could be further extended to include
        first and last names separately or additional metadata.
    """

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        """Return a human readable representation of the author."""
        return self.name


class Book(models.Model):
    """Represents a book written by an ``Author``.

    Fields
    ------
    title : CharField
        The title of the book.  Stored as text up to 255 characters.
    publication_year : IntegerField
        Four‑digit year indicating when the book was published.  A
        custom validator in the serializer ensures this is not in
        the future.
    author : ForeignKey to Author
        Creates a many‑to‑one relationship where each book is
        associated with exactly one author.  The ``related_name``
        ``'books'`` allows reverse access from authors to their
        associated books via ``author.books.all()``.
    """

    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return a human readable representation of the book."""
        return self.title
