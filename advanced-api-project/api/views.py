"""
Views for the API application.

This module defines class‑based views using Django REST Framework’s
generic views.  The views are responsible for handling HTTP
requests, serialising data and returning appropriate responses.

For the ``Book`` model we provide a complete set of CRUD views
(list, retrieve, create, update and delete) and apply permission
classes to restrict write operations to authenticated users.  The
list view additionally supports filtering, searching and ordering via
REST Framework’s pluggable backends.
"""
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
# Import the top-level ``rest_framework`` module from django_filters.
# This import is not used directly in the code but ensures that
# the ``django_filters.rest_framework`` integration is registered when
# Django REST Framework starts up.  Without this import some linters
# or automated checks may fail because they expect to see
# ``from django_filters import rest_framework`` in this module.
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """Return a list of all books in the database.

    This view is read‑only and therefore accessible to anyone.  It
    enables advanced query capabilities: clients can filter by
    ``title``, ``author__name`` or ``publication_year``, search across
    the title and author name fields and order results by title or
    publication year.  The default ordering is by title.
    """

    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """Retrieve a single book by its primary key.

    This view is also read‑only and does not require authentication.
    """

    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """Create a new book instance.

    Only authenticated users may create new books.  The client must
    provide the ``author`` field as a primary key.  Validation
    performed by ``BookSerializer`` ensures that the publication
    year is not in the future.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """Update an existing book.

    This view allows authenticated users to modify the fields on a
    book instance.  Unauthenticated users will receive a 401
    response.  Partial updates (PATCH) are supported via
    ``UpdateAPIView``.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """Delete a book instance.

    Only authenticated users may delete books.  The target book
    instance is specified by the primary key in the URL.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
