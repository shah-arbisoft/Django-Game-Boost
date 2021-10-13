
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.http import request
from django.utils.translation import ugettext as _

# from django.forms import fields
from accounts.models import User


class ProfileUpdateForm(forms.Form):

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request' , None)
    #     super(ProfileUpdateForm, self).__init__(*args, **kwargs)

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

    
    def clean_confirm_password(self):
        cleaned_data = self.cleaned_data
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password:
            if new_password != confirm_password:
                # self.add_error('confirm_password', _("Passwords did not match"))
                raise ValidationError(_("Passwords did not match"))
        return cleaned_data

    
    
    # def save(self, commit=True):
    #     print(commit.get("request").user)
    #     print(self.request)
    #     cleaned_data = super().clean()
    #     request = self.request
    #     user = request.user
    #     if cleaned_data.get('full_name'):
    #         user.full_name = cleaned_data.get('full_name')
    #     if cleaned_data.get('cnic'):
    #         user.cnic = cleaned_data.get('cnic')
    #     if cleaned_data.get('credit_card'):
    #         user.credit_card_number = cleaned_data.get('credit_card')
    #     # if cleaned_data.get('date_of_birth') != "":
    #     #     print(cleaned_data.get('date_of_birth'))
    #     #     user.date_of_birth = cleaned_data.get('date_of_birth')
    #     if cleaned_data.get('age'):
    #         user.age = cleaned_data.get('age')
    #     if cleaned_data.get('about_info'):
    #         user.about_info = cleaned_data.get('about_info')
    #     if request.POST.get('profile_image'):
    #         user.profile_image = request.FILES['profile_image']
    #     return user
        

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
