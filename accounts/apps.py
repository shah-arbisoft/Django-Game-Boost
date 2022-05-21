"""Apps can be configure in this module."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """To configure App "Account" """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
