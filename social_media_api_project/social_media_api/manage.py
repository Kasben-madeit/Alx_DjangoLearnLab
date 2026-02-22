#!/usr/bin/env python
"""
This script is the entry point for administrative tasks for the
`social_media_api` Django project.  It sets the default settings
module and then delegates to Django’s management utility.

You should not need to modify this file to work through the lab
exercises.  If you encounter an error about Django not being
installed, ensure that you have activated a virtual environment and
installed the dependencies listed in ``requirements.txt``.
"""

import os
import sys


def main() -> None:
    """Run administrative tasks."""
    # Point Django at the settings for this project.  When deploying
    # to production you can override this with the DJANGO_SETTINGS_MODULE
    # environment variable.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
    try:
        from django.core.management import execute_from_command_line  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()