from django.contrib import admin

from games.models import Category, Game

from .models import Category, Game, SellerGame

# Register your models here.
admin.site.register(Game)
admin.site.register(Category)
admin.site.register(SellerGame)

