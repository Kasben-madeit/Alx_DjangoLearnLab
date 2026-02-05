"""
Unit tests for the API application.

These tests use Django’s built‑in test framework together with
Django REST Framework’s APITestCase to simulate HTTP requests against
the API views.  The tests cover the full CRUD lifecycle on the
``Book`` model, ensure that permissions are enforced correctly and
verify that filtering, searching and ordering behave as expected.
"""
from datetime import date
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """Comprehensive test suite for the Book API endpoints."""

    def setUp(self) -> None:
        # Create a test author and a book
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=date.today().year - 1,
            author=self.author,
        )
        # Create a user used for authenticated requests
        User = get_user_model()
        self.user = User.objects.create_user(username='user', password='pass')

    def test_list_books(self) -> None:
        """Ensure that the list endpoint returns all books with a 200 status."""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The response should be a list with one book
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book.title)

    def test_retrieve_book(self) -> None:
        """Ensure that retrieving a single book returns the correct data."""
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_create_book_requires_authentication(self) -> None:
        """Unauthenticated users should not be allowed to create books."""
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': date.today().year - 2,
            'author': self.author.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book(self) -> None:
        """Authenticated users can create a new book and receive a 201 status."""
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': date.today().year - 2,
            'author': self.author.id,
        }
        # Log in the test user via the client.  Using ``login`` instead of
        # ``force_authenticate`` exercises the full authentication stack and
        # ensures that session and authentication middleware are engaged.
        self.client.login(username=self.user.username, password='pass')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Book')

    def test_create_book_invalid_publication_year(self) -> None:
        """Attempting to create a book with a future publication year should fail."""
        url = reverse('book-create')
        future_year = date.today().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.id,
        }
        # Authenticate the user with ``login`` to perform the request
        self.client.login(username=self.user.username, password='pass')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

    def test_update_book(self) -> None:
        """Authenticated users can update an existing book using PUT."""
        url = reverse('book-update', args=[self.book.id])
        data = {
            'title': 'Updated Title',
            'publication_year': self.book.publication_year,
            'author': self.author.id,
        }
        # Use ``login`` to authenticate instead of ``force_authenticate``
        self.client.login(username=self.user.username, password='pass')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh from DB and verify the change
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    def test_delete_book(self) -> None:
        """Authenticated users can delete a book and receive a 204 status."""
        url = reverse('book-delete', args=[self.book.id])
        # Authenticate via ``login`` to ensure session handling is used
        self.client.login(username=self.user.username, password='pass')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_search_and_ordering(self) -> None:
        """Filtering, searching and ordering should return the expected subset."""
        # Create a second book to exercise filtering
        Book.objects.create(
            title='Another Book',
            publication_year=date.today().year - 3,
            author=self.author,
        )
        # Filter by title
        url = reverse('book-list') + '?title=Another%20Book'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Another Book')
        # Search by partial title
        url = reverse('book-list') + '?search=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should include only books with 'Test' in their title
        titles = [item['title'] for item in response.data]
        self.assertIn('Test Book', titles)
        # Ordering by publication year descending
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [item['publication_year'] for item in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
