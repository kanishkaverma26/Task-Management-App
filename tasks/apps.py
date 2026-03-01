from django.apps import AppConfig


class TasksConfig(AppConfig):
    """
    Application configuration for the Tasks app.

    This class defines the default settings for the app,
    including the default primary key field type and
    the application name used by Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
