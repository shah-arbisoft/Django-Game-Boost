from django import forms
from django.db import models
from django.db.models import fields
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext as _

from .models import SellerGame


class AddGame(forms.ModelForm):
    class Meta:
        model = SellerGame
        fields = "__all__"
        widgets={'seller': HiddenInput()}