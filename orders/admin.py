"""Models to be displayed on Admin panel are registered here"""

from django.contrib import admin

# pylint: disable=relative-beyond-top-level
from .models import Order, Review

admin.site.register(Order)
admin.site.register(Review)
