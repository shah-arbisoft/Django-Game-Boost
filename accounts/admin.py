"""Models to be displayed on Admin panel are registered here"""

from django.contrib import admin

# pylint: disable=relative-beyond-top-level, invalid-name
from .models import Buyer, Seller, User


admin.site.register(User)
admin.site.register(Buyer)
admin.site.register(Seller)
