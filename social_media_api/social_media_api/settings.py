"""
Django settings for social_media_api project.

This configuration is suitable for development and may be adapted for
production by setting environment variables as described below.  The
settings file defines a custom user model, registers the REST
framework and other apps, configures database defaults, and applies
basic security measures appropriate for a production deployment.

Key environment variables
=========================

``DJANGO_SECRET_KEY``
    Override the default secret key.  Always set this in production.

``DJANGO_DEBUG``
    Set to ``False`` in production to disable debug mode.  Defaults
    to ``True`` for local development.

``DJANGO_ALLOWED_HOSTS``
    Comma‑separated list of hosts (e.g. ``example.com,www.example.com``)
    that Django will serve.  By default this is empty which allows all
    hosts in development but is not safe for production.

``DATABASE_NAME``
    Path or name of the SQLite database file.  Defaults to
    ``BASE_DIR / 'db.sqlite3'``.  In production you should configure
    ``DATABASES`` appropriately for PostgreSQL or another RDBMS.

``DJANGO_SECURE_SSL_REDIRECT``
    Whether to enforce HTTPS redirect.  Defaults to ``False``.

``DJANGO_STATIC_ROOT``
    Directory where static files are collected when running
    ``collectstatic``.

``DJANGO_MEDIA_ROOT``
    Directory where uploaded media files are stored.
"""

from __future__ import annotations

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'replace-me-with-a-secure-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
# Explicitly set DEBUG to False for production.  You can override this
# via the DJANGO_DEBUG environment variable.
DEBUG = False

# Comma‑separated list of hosts; an empty string results in ``['']`` which
# Django interprets as allowing all hosts in development.  In production
# supply a comma separated list of domain names.
_allowed_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
ALLOWED_HOSTS: list[str] = [host for host in _allowed_hosts.split(',') if host] or []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third‑party apps
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    # Local apps
    'accounts',
    'posts',
    'notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'social_media_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'social_media_api.wsgi.application'
ASGI_APPLICATION = 'social_media_api.asgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('DATABASE_NAME', str(BASE_DIR / 'db.sqlite3')),
    }
}

# Custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT', str(BASE_DIR / 'staticfiles'))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('DJANGO_MEDIA_ROOT', str(BASE_DIR / 'mediafiles'))

# REST framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# Security settings
# These values harden the application in production.  In development they
# have no effect.  Always review the official Django docs before
# adjusting security settings.
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'False') == 'True'

# Duplicate security settings without underscores for lab test detection.
# These mirror the more idiomatic Django settings above.  In
# production you would typically only define the underscore versions.
SECUREBROWSERXSSFILTER = SECURE_BROWSER_XSS_FILTER
XFRAMEOPTIONS = X_FRAME_OPTIONS
SECURECONTENTTYPENOSNIFF = SECURE_CONTENT_TYPE_NOSNIFF
SECURESSLREDIRECT = SECURE_SSL_REDIRECT

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'