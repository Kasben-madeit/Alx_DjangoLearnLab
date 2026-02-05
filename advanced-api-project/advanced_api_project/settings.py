"""
Django settings for advanced_api_project.

This settings module configures the Django project with a minimal
configuration suitable for development and testing.  It uses
SQLite for the database backend and includes the Django REST
Framework and Django Filter as third‑party dependencies.  For
production deployment you should override settings like ``SECRET_KEY``
and ``DEBUG`` using environment variables.
"""
from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# This hard coded key is fine for development and testing but should
# be replaced in production.  The surrounding quotes allow hyphens
# in the project directory name but do not affect the key value.
SECRET_KEY: str = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-me')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Allow all hosts during development.  In production you should
# restrict this list to your domain names.
ALLOWED_HOSTS: list[str] = []

# Application definition
INSTALLED_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third‑party apps
    'rest_framework',       # Django REST Framework for building APIs
    'django_filters',       # Filtering support used by REST Framework
    # Local apps
    'api',
]

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration module for the project
ROOT_URLCONF: str = 'advanced_api_project.urls'

# Template configuration.  The project does not define any custom
# templates directories, relying solely on app templates.
TEMPLATES: list[dict[str, object]] = [
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

# WSGI application path
WSGI_APPLICATION: str = 'advanced_api_project.wsgi.application'

# Database configuration: use SQLite by default.  To use another
# database backend, override the ``ENGINE`` and other settings via
# environment variables or a separate settings module.
DATABASES: dict[str, dict[str, object]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
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
LANGUAGE_CODE: str = 'en-us'
TIME_ZONE: str = 'UTC'
USE_I18N: bool = True
USE_TZ: bool = True

# Static files (CSS, JavaScript, Images)
STATIC_URL: str = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

# Django REST Framework default settings.  These can be overridden
# on a per-view basis.  We enable filtering, search and ordering
# globally.
REST_FRAMEWORK: dict[str, object] = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}
