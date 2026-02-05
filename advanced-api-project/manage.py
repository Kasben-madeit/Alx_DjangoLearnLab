#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script is the canonical entry point for interacting with the
project.  It sets the `DJANGO_SETTINGS_MODULE` environment variable
to point at the settings module and then delegates to
``django.core.management``.
"""
import os
import sys


def main() -> None:
    """Run administrative tasks."""
    # Point Django at our settings module.  Using an underscore in the
    # package name avoids the `-` character which is invalid in Python
    # identifiers.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover - will raise if Django isn't installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your "
            "PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()