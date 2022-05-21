"""Models to be displayed on Admin panel are registered here"""

from django.contrib import admin

# pylint: disable=relative-beyond-top-level, invalid-name
from .models import Category, Game, SellerGame

# Register your models here.
admin.site.register(Game)
admin.site.register(Category)
admin.site.register(SellerGame)
