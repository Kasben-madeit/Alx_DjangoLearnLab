from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self):
        # Import signals to create user profiles automatically
        try:
            import blog.signals  # noqa: F401
        except ImportError:
            pass