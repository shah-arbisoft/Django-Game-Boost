"""Forms to be defined for model User, Buyer and Seller in this module."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from accounts.models import User


class ProfileUpdateForm(forms.Form):
    """A Form for User to update his info"""

    age = forms.IntegerField(label="Age", max_value=120, required=False)
    profile_image = forms.ImageField(label="Profile Image", required=False)
    date_of_birth = forms.DateTimeField(label="Date of Birth", required=False)

    full_name = forms.CharField(
        label="Full Name", max_length=50, required=False
    )
    user_name = forms.CharField(
        label='User name', max_length=50, required=False, disabled=True
    )
    email = forms.EmailField(
        label='Email', max_length=100, required=False, disabled=True
    )
    joining_date = forms.DateTimeField(
        label="Date of joining", required=False, disabled=True
    )
    about_info = forms.CharField(
        label="About Info",
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False
    )

    cnic = forms.CharField(
        label="CNIC", max_length=15, required=False
    )
    credit_card = forms.CharField(
        label="Credit Card", max_length=24, required=False
    )

    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(),
        required=False, min_length=8
    )
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(),
        required=False, min_length=8
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(),
        required=False, min_length=8
    )

    def clean(self):
        """
        While User is updating his info, if he tries to change his
        password, Form is validated for fields Current Pasword and
        Confirm Password to ensure that User has not made a mistake
        while setting his new password.
        """
        cleaned_data = self.cleaned_data
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password:
            if new_password != confirm_password:
                raise ValidationError(_("Passwords did not match"))
        return cleaned_data

    def _update_current_user_password(self, user):
        """
        To change User password, current password from database and Form is
        compared, if they matched then new password is saved as new passowrd
        in database, else ValidationError is raised for unmatched current password.

        Args:
            user (USER):
                Current logged-in user who wants to update his password
        Returns:
            USER:
                Same user is returned with updated password
        """
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        if user.check_password(current_password):
            user.set_password(cleaned_data.get("new_password"))
            return user
        raise ValidationError("Current Password is incorrect")

    def save(self, request):
        """
        Updated values are fetched from Form after validation is applied on each
        field and if any new information is recieved then update User with it.
        """
        cleaned_data = super().clean()
        user = request.user
        if cleaned_data.get('full_name'):
            user.full_name = cleaned_data.get('full_name')
        if cleaned_data.get('cnic'):
            user.cnic = cleaned_data.get('cnic')
        if cleaned_data.get('credit_card'):
            user.credit_card_number = cleaned_data.get('credit_card')
        if len(request.FILES):
            user.profile_image = request.FILES['profile_image']
        if cleaned_data.get('age'):
            user.age = cleaned_data.get('age')
        if cleaned_data.get('about_info'):
            user.about_info = cleaned_data.get('about_info')
        if cleaned_data.get("current_password"):
            user = self._update_current_user_password(user)
        user.save()


class SignupForm(UserCreationForm):
    """A signup form for a new user to create a new account and register."""

    def __init__(self, *args, **kwargs):
        """Before initialzing this Form, some fields are modified to be used."""
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input100'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    email = forms.EmailField(label='Email', max_length=100)
    user_name = forms.CharField(label='User Name', max_length=85)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput()
    )

    class Meta:
        """Defing Form behaviour"""
        model = User
        fields = ('email', 'user_name', 'password1', 'password2')
