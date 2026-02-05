# Advanced API Project

This project demonstrates how to build a small Django REST Framework API
from scratch.  The goal is to illustrate a clean architecture for
maintaining models, serializers, generic views, permissions and tests
while keeping the code well documented.  The project exposes a
simple catalog of authors and books, but the patterns used here can
serve as a solid foundation for more complex APIs.

## Project layout

The repository is organised as a normal Django project created via
`django‑admin startproject`.  A top‑level folder `advanced_api_project`
contains the Django settings, URL configuration and WSGI/ASGI entry
points.  A separate application called `api` lives alongside
`advanced_api_project` and holds all domain logic.

```
advanced-api-project/
├── README.md                 ← this file
├── requirements.txt          ← third‑party dependencies
├── manage.py                 ← Django management entry point
├── advanced_api_project/     ← project package (settings, urls)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── api/                      ← reusable application
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── test_views.py
```

### Models

Two models are defined in `api/models.py`:

* **Author** – represents an author with a single `name` field.
* **Book** – represents a book with a `title`, a `publication_year`
  and a foreign key `author` pointing back to the `Author` model.

Each model includes a helpful `__str__` method for debugging and is
registered in the admin site in `api/admin.py`.

### Serializers

Serializers live in `api/serializers.py` and are responsible for
converting model instances into Python primitives that can be
rendered into JSON.  Two serializers are provided:

* **BookSerializer** – serializes all fields on the `Book` model and
  includes a custom validation method to ensure that the
  `publication_year` is not in the future.
* **AuthorSerializer** – exposes the author `name` along with a
  nested list of the author’s books.  Nesting is achieved by
  embedding a `BookSerializer` as a read‑only field so that the API
  returns full book details when fetching an author.

Both serializers include inline comments explaining the purpose of
each field and how nested relationships are handled.

### Generic views and URL routing

The `api/views.py` file defines a set of class‑based generic views
for the `Book` model using Django REST Framework’s
`ListAPIView`, `RetrieveAPIView`, `CreateAPIView`, `UpdateAPIView`
and `DestroyAPIView` classes.  These views handle listing all books,
retrieving a single book, creating a new book, updating an existing
book and deleting a book respectively.  Permissions are applied so
that read‑only operations (`List` and `Retrieve`) are available to
unauthenticated users, while mutating operations (`Create`, `Update`
and `Destroy`) require authentication.

Filtering, searching and ordering are enabled on the list view via
`DjangoFilterBackend`, `SearchFilter` and `OrderingFilter`.  Users
can filter books by title, author name or publication year, search
across title and author name fields and order the result set by
title or publication year.

Corresponding URL patterns are configured in `api/urls.py` and
included from the project’s root `urls.py` under the `/api/`
namespace.  Each view is assigned a descriptive name to make reverse
lookups in tests straightforward.

### Tests

Unit tests are located in `api/test_views.py`.  They leverage
Django’s built‑in test framework along with `rest_framework`’s
`APITestCase` to simulate HTTP requests against the API.  The tests
cover the full CRUD lifecycle on the `Book` model and ensure that
filtering, searching, ordering and permission checks behave as
expected.  Running the tests is as simple as executing

```
python manage.py test api
```

## Running the project

To set up the project locally you will need Python 3.11 or later.  It
is recommended to create a virtual environment and install the
dependencies listed in `requirements.txt`:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run migrations to create the database tables and start the
development server:

```
python manage.py migrate
python manage.py runserver
```

You can then interact with the API at `/api/books/` and `/api/books/<id>/`.
