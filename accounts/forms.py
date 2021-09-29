# class CreateUser(Us)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import widgets
# from django.forms import fields
from accounts.models import User
from django.utils.translation import ugettext as _


class ProfileUpdateForm(forms.Form):
    full_name = forms.CharField(label="Full Name", max_length=50, required=False)
    user_name = forms.CharField(label='User name', max_length=50, required=False, disabled=True)
    email = forms.EmailField(label='Email', max_length=100, required=False, disabled=True)
    cnic = forms.CharField(label="CNIC", max_length=15, required=False)
    credit_card = forms.CharField(label="Credit Card", max_length=24, required=False)
    age = forms.IntegerField(label="Age", max_value=120, required=False)
    profile_image = forms.ImageField(label="Profile Image", required=False)
    date_of_birth = forms.DateTimeField(label="Date of Birth", required=False)
    joining_date = forms.DateTimeField(label="Date of joining", required=False, disabled=True)
    about_info = forms.CharField(label="About Info", widget=forms.Textarea(attrs={'rows':5}), required=False)
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput(), required=False, min_length=8)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(), required=False, min_length=8)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(), required=False, min_length=8)

    def save(self, *args, **kwargs):
        pass
    def clean_confirm_password(self):
        cleaned_data = self.cleaned_data
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password:
            if new_password != confirm_password:
                # self.add_error('confirm_password', _("Passwords did not match"))
                raise ValidationError(_("Passwords did not match"))
        return cleaned_data




class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input100'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    email = forms.EmailField(label='Email', max_length=100)
    user_name = forms.CharField(label='User Name',max_length=85)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'user_name', 'password1', 'password2')
