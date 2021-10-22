"""Apps can be configure in this module."""

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """App Order is to be configured"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
