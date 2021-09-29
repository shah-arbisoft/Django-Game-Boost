"""Contains all the view fucntions."""

# pylint: disable=relative-beyond-top-level
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ProfileUpdateForm, SignupForm


def signup(request):
    """
    To Create new Account, It first checks if USER is autheticated then
    redirect him to HOME page, If not then create SignupForm. And if request
    is a POST request then save the form after validating it, Account will be
    created and redirect user to Login Page.
    """
    if request.user.is_authenticated:
        return redirect('accounts:home')
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Successfully Create')
            return redirect(reverse('accounts:login'))
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='accounts:login')
def home(request):
    """
    If User is logged-in then, if User is superuser then redirect him to
    Admin panel, else return rendered home.html template.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    return render(request, 'home.html')


def login_user(request):
    """
    If user is logged in then redirect him to Home page, else if user is
    autheticated then User is logged in but if authenction failed then error
    message is displayed. If User is superuser then redirect him
    to admin panel.

    TEMPLATE:
        login.html
    """
    if request.user.is_authenticated:
        return redirect('accounts:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                messages.info(request, 'Logged in as a Super User')
                return redirect('admin:login')
            return redirect(reverse('accounts:home'))
        messages.info(request, 'Username or Password is incorrect')
    return render(request, 'login.html')


def logout_user(request):
    """
    It will Log out User and redirect him to Login page along success message.
    """
    logout(request)
    messages.info(request, 'Log out successful')
    return redirect(reverse('accounts:login'))


def get_user_profile_details(request):
    """
    It will return rendered template 'profile.html' along with form
    whenever this function is called.
    """
    form = ProfileUpdateForm()
    return render(request, "profile.html", {"form": form})


def update_user_with_form_fields_data(request, cleaned_data, user):
    """
    Updated values are fetched from Form after validation is applied on each
    field and if any new information is recieved then update User with it.
    """
    if cleaned_data.get('full_name'):
        user.full_name = cleaned_data.get('full_name')
    if cleaned_data.get('cnic'):
        user.cnic = cleaned_data.get('cnic')
    if cleaned_data.get('credit_card'):
        user.credit_card_number = cleaned_data.get('credit_card')
    # if cleaned_data.get('date_of_birth') != "":
    #     print(cleaned_data.get('date_of_birth'))
    #     user.date_of_birth = cleaned_data.get('date_of_birth')
    if cleaned_data.get('age'):
        user.age = cleaned_data.get('age')
    if cleaned_data.get('about_info'):
        user.about_info = cleaned_data.get('about_info')
    if request.POST.get('profile_image'):
        user.profile_image = request.FILES['profile_image']
    return user


def update_current_user_password(request, user):
    """
    To change User password, current password from database and Form is
    compared, if they matched then new password is saved as new passowrd
    in database, else ValidationError is raised for unmatched current password.
    """
    current_password = request.POST.get("current_password")
    if user.check_password(current_password):
        user.set_password(request.POST.get("new_password"))
        return user
    raise ValidationError("Current Password is incorrect")


@login_required(login_url='accounts:login')
def update_user_profile(request):
    """
    To update User profile details, updated data is fetched from Form after a
    User makes a POST request and User profile is updated in Database with new
    Values. If any errors from Form validation fails will be shown.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = request.user
            updated_user = update_user_with_form_fields_data(
                request, cleaned_data, user
            )
            if request.POST.get("current_password"):
                updated_user = update_current_user_password(request, user)
            updated_user.save()
        else:
            print(form.errors)
    return redirect("accounts:home")
