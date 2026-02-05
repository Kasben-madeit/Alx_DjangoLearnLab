"""
ASGI config for advanced_api_project.

This exposes the ASGI callable as a module-level variable named
``application``.  For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/.
"""
import os
from django.core.asgi import get_asgi_application


# Set the default settings module for the 'asgi' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')

# Create the ASGI application object which will be used by any ASGI
# servers configured to use this file.
application = get_asgi_application()
