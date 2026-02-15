# Django Blog Project – ALX Django Learn Lab

This repository contains a simple yet fully‑featured blogging application built
with Django.  The project serves as a practical demonstration of key web
development concepts including user authentication, CRUD operations, comments,
tagging and search functionality.  It is organised as a Django project named
`django_blog` with a single application named `blog`.

## Features

### Project Setup

* The project is configured to use SQLite by default, requiring no additional
  database setup.  To switch to PostgreSQL or another database, edit the
  `DATABASES` setting in `django_blog/settings.py`.
* Static files are served from the `static/` directory and templates are
  collected in `templates/`.
* A placeholder `SECRET_KEY` is provided for educational purposes.  **Do not**
  use this key in production.

### User Authentication

* Users can register for new accounts via the `/register/` route.  Registration
  uses a custom form that extends `UserCreationForm` to include an email
  address.
* Login and logout are handled by Django’s built‑in authentication views.  The
  templates for login and logout are located under `templates/registration/`.
* Upon successful registration, a `Profile` object is automatically created
  thanks to model signals defined in `blog/signals.py`.
* Authenticated users can view and edit their profile at `/profile/`.  The
  profile includes a bio and optional profile picture.

### Blog Posts

* Users can create, view, edit and delete blog posts.  Posts consist of a
  title, rich text content, publication timestamp and author.
* Only the author of a post can edit or delete it; this is enforced via the
  `UserPassesTestMixin` in the update and delete views.
* Posts can be tagged with multiple keywords.  Tags are created on the fly
  from a comma‑separated list entered in the post form.
* The home page lists posts in reverse chronological order and supports
  pagination.

### Comments

* Authenticated users can leave comments on any post.  Comments support basic
  editing and deletion, but only by their author.
* All comments for a post are displayed beneath its content on the post detail
  page.

### Tagging and Search

* Tags allow posts to be categorised.  Clicking a tag on a post links to a
  page listing all posts associated with that tag.
* A simple search form in the navigation bar lets users search for posts by
  title, content and tag names.  The search results page displays any matches.

## Running the Project

To run the development server locally, navigate into the `django_blog` folder
and execute:

```bash
python manage.py migrate  # create database tables
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to see the blog in action.  You
can register a new user, create posts, leave comments and explore tagging and
search functionality.

## Tests and Limitations

This code has been written without running in a live Django environment due to
the limitations of the execution environment.  Although every effort has been
made to adhere to Django best practices and syntax, minor adjustments may be
required when running in a real environment.  Feel free to open issues or
submit pull requests if you encounter any problems.