"""
Configuration for the API application.

The ``ApiConfig`` class declares default auto field type and
specifies the dotted path to the application.  Django uses this
configuration to initialise the app when the project starts.
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'api'
