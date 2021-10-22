"""Forms to be defined related to model Game in this module."""

from django import forms
from django.forms.widgets import HiddenInput

# pylint: disable=relative-beyond-top-level, invalid-str-returned, too-few-public-methods
from .models import SellerGame


class AddGame(forms.ModelForm):
    """A Form for Seller to add a Game to his list of games he offer service."""
    class Meta:
        """Changing default Model behaviour"""
        model = SellerGame
        fields = "__all__"
        widgets = {'seller': HiddenInput()}
