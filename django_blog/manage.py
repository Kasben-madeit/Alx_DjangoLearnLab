#!/usr/bin/env python3
"""
Django's command-line utility for administrative tasks.

This file is generated as part of the ALX Django blog project. It provides a
command-line entry point for performing common Django management tasks such
as starting the development server, running migrations and creating app
structures. See the Django documentation for full details.
"""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_blog.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
