# Social Media API

## Overview

This project is a fully‑fledged social media API built with **Django** and
**Django REST Framework (DRF)**.  It demonstrates how to build a
custom user model, implement token‑based authentication, and layer on
social features such as posts, comments, likes, follows, feeds and
notifications.  The API is designed for educational purposes but
provides a solid starting point for a production application.

The repository is organised as a Django project named
`social_media_api` which contains three apps:

* **accounts** – Custom user model, registration, login, profile
  management and follow/unfollow functionality.
* **posts** – CRUD operations for posts and comments, like/unlike
  endpoints and a personalised feed of posts from followed users.
* **notifications** – Generic activity notifications generated when
  users follow one another, like posts or comment on posts.

All endpoints are prefixed with `/api/` or `/api/auth/` for clarity.

---

## Getting Started

### Prerequisites

* Python 3.9 or later
* A recent version of **pip** (see `requirements.txt` for dependency
  versions)
* [virtualenv](https://virtualenv.pypa.io/) or a similar tool is
  recommended for local development.

### Installation

1. **Clone the repository** (if you haven't already):

   ```bash
   git clone https://github.com/your-username/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/social_media_api
   ```

2. **Create and activate a virtual environment** (optional but
   recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

You can now interact with the API at `http://127.0.0.1:8000/`.

---

## API Endpoints

All API responses are JSON.  Authentication is handled via DRF's
token authentication.  After registration or login, include the
header `Authorization: Token <your-token>` in subsequent requests.

### Authentication and User Management (`/api/auth/`)

| Method | Endpoint                          | Description                               |
| ------ | ---------------------------------- | ----------------------------------------- |
| POST   | `/api/auth/register/`             | Register a new user and receive a token.  |
| POST   | `/api/auth/login/`                | Log in with existing credentials.         |
| GET    | `/api/auth/profile/`              | Retrieve the authenticated user's profile.|
| PUT    | `/api/auth/profile/`              | Update the authenticated user's profile.  |
| POST   | `/api/auth/follow/<user_id>/`     | Follow another user.                      |
| POST   | `/api/auth/unfollow/<user_id>/`   | Unfollow a user.                          |

#### Registration

Send a POST request with `username`, `email` and `password` to
`/api/auth/register/`.  On success you will receive a token and user
profile.  Example:

```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "alice",
  "email": "alice@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "token": "e5b2c8...",
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "bio": "",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0
  }
}
```

#### Login

Send a POST request with `username` and `password` to `/api/auth/login/`.
You will receive an existing or newly created token along with the
user profile.

#### Profile

You can retrieve or update your own profile via GET or PUT requests
to `/api/auth/profile/`.  Updates allow you to modify the `bio` or
upload a `profile_picture`.  The picture should be uploaded as
multipart/form-data.

#### Follow/Unfollow

To follow another user send a POST request to `/api/auth/follow/<user_id>/`.
To unfollow send a POST request to `/api/auth/unfollow/<user_id>/`.
These actions generate a notification for the target user.

### Posts and Comments (`/api/`)

| Method | Endpoint                                   | Description                                             |
| ------ | ------------------------------------------- | ------------------------------------------------------- |
| GET    | `/api/posts/`                              | List all posts.  Supports search on title and content. |
| POST   | `/api/posts/`                              | Create a new post.                                      |
| GET    | `/api/posts/<id>/`                         | Retrieve a single post with nested comments.           |
| PUT    | `/api/posts/<id>/`                         | Update a post (author only).                            |
| DELETE | `/api/posts/<id>/`                         | Delete a post (author only).                            |
| GET    | `/api/posts/<post_id>/comments/`           | List comments on a post.                                |
| POST   | `/api/posts/<post_id>/comments/`           | Add a comment to a post.                                |
| GET    | `/api/posts/<post_id>/comments/<id>/`      | Retrieve a specific comment.                            |
| PUT    | `/api/posts/<post_id>/comments/<id>/`      | Update a comment (author only).                         |
| DELETE | `/api/posts/<post_id>/comments/<id>/`      | Delete a comment (author only).                         |
| POST   | `/api/posts/<id>/like/`                    | Like a post.  Returns an error if already liked.        |
| POST   | `/api/posts/<id>/unlike/`                  | Remove your like from a post.                           |
| GET    | `/api/feed/`                               | Retrieve recent posts from users you follow.            |

#### Pagination and Filtering

List endpoints are paginated with a default page size of 10 items.  Use the
`page` query parameter to retrieve further pages.  Posts support
searching by title or content via the `search` query parameter.

#### Likes

To like a post send a POST request to `/api/posts/<id>/like/`.  If you
attempt to like the same post twice you will receive a 400 error.
Unliking uses `/api/posts/<id>/unlike/`.  When someone likes one of
your posts you will receive a notification.

### Notifications (`/api/notifications/`)

| Method | Endpoint                    | Description                                    |
| ------ | --------------------------- | ---------------------------------------------- |
| GET    | `/api/notifications/`       | List all notifications for the authenticated user. |

Notifications are created when:

* Another user follows you
* Someone likes one of your posts
* Someone comments on your post

Each notification records the actor, a verb (e.g. "followed", "liked",
"commented"), an optional target object and a timestamp.  You can mark
notifications as read by extending the API with a custom endpoint.

---

## Deployment Guide

While this project is set up for local development by default, it
includes configuration points that make it straightforward to deploy
to a production environment such as **Heroku**, **AWS Elastic
Beanstalk**, **Render**, **DigitalOcean** or any other platform that
supports running Django applications.  Below are some general steps
for deployment.

1. **Set environment variables**.  At minimum set
   `DJANGO_SECRET_KEY` to a strong random value and `DJANGO_DEBUG` to
   `False`.  Specify `DJANGO_ALLOWED_HOSTS` with your domain name(s)
   separated by commas.

2. **Configure a production database**.  Update the `DATABASES`
   setting via environment variables or modify the configuration in
   `social_media_api/settings.py` to point at PostgreSQL or another
   database backend.  Many hosting providers offer managed PostgreSQL
   services.

3. **Collect static files**.  Run `python manage.py collectstatic` to
   gather static assets into the directory specified by
   `DJANGO_STATIC_ROOT`.  In production you should serve static files
   via a web server or object storage (e.g. AWS S3).

4. **Use a production WSGI server**.  The included `requirements.txt`
   specifies **Gunicorn**, a Python WSGI HTTP server.  You can run
   Gunicorn directly in many deployment environments:

   ```bash
   gunicorn social_media_api.wsgi --bind 0.0.0.0:$PORT
   ```

   Replace `$PORT` with the port provided by your hosting platform.

5. **Configure a reverse proxy**.  In many cases you will deploy
   behind Nginx or an equivalent reverse proxy.  This server should
   handle HTTPS termination and serve your collected static files.

6. **Provision media storage**.  If your users upload profile
   pictures, configure `MEDIA_ROOT` to point to a durable storage
   location such as AWS S3.  Tools like
   [`django-storages`](https://django-storages.readthedocs.io/) can
   simplify this setup.

7. **Monitoring and maintenance**.  Set up logging and error
   reporting using tools such as Sentry or Prometheus.  Regularly
   apply security updates to Django and other dependencies.

---

## Running Tests

This repository does not include automated tests out of the box,
but you can add your own using Django’s built‑in testing framework or
third‑party tools such as **pytest**.  To run tests once you have
created them:

```bash
python manage.py test
```

---

## Contributing

Contributions are welcome!  Feel free to fork the repository and open
pull requests.  If you discover bugs or have suggestions for
improvements, please create an issue.

---

## License

This project is licensed under the MIT License.  See the `LICENSE`
file for details.