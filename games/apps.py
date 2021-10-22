"""Apps can be configure in this module."""

from django.apps import AppConfig


class GamesConfig(AppConfig):
    """To configure App "Game" """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'games'
