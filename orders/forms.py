"""Forms to be defined for 'model' Order in this module."""

from django.forms import ModelForm

# pylint: disable=relative-beyond-top-level, too-few-public-methods
from .models import Order


class PlaceOrder(ModelForm):
    """Defining Model Form for our model Order"""

    class Meta:
        """Defing Form behaviour"""
        model = Order
        fields = '__all__'
        exclude = ['status']
