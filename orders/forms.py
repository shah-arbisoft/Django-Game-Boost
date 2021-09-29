from django.forms import ModelForm, fields
from .models import Order

class PlacingOrder(ModelForm):
    class Meta:
        model = Order
        fields = [
            "gaming_account_id", "gaming_account_password", "price",
            "description", "number_of_days_for_completing_the_order", "game"
        ]