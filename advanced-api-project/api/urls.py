"""
URL patterns for the API application.

This module defines the routing for all API endpoints related to
``Book`` instances.  Each view is associated with a path and a
name, allowing for reverse URL lookups in tests and templates.

Paths
-----
* ``/books/`` – list all books (GET).
* ``/books/<int:pk>/`` – retrieve a single book (GET).
* ``/books/create/`` – create a new book (POST).
* ``/books/<int:pk>/update/`` – update an existing book (PUT/PATCH).
* ``/books/<int:pk>/delete/`` – delete a book (DELETE).
"""
from django.urls import path
from . import views


urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]
