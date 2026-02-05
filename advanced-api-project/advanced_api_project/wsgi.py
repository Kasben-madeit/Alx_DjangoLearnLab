"""
WSGI config for advanced_api_project.

This exposes the WSGI callable as a module-level variable named
``application``.  For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/.
"""
import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'wsgi' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')

# Create the WSGI application object which will be used by any WSGI
# servers configured to use this file.
application = get_wsgi_application()
