"""This module contains all url paths for our app Order"""

from django.urls import path

# pylint: disable=relative-beyond-top-level, invalid-name
from . import views

app_name = "orders"
urlpatterns = [
    path('place_order/', views.create_order, name='creating_order'),
    path('my_orders/', views.show_all_orders_of_current_user, name='my_orders'),
]
