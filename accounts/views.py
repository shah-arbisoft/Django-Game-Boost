"""Contains all the view fucntions."""

# pylint: disable=relative-beyond-top-level
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
# from django.views.generic.detail import DetailView
from django.db.models import Avg, Count, Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.models import Seller, User
from games.models import Game, SellerGame
from games.signals import game_clicked_signal

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


# @login_required(login_url='accounts:login')
# def show_all_users(request):
#     """
#     If User is logged-in then, if User is superuser then redirect him to
#     Admin panel, else return Users template.
#     """
#     if request.user.is_superuser:
#         return redirect('admin:login')
#     context = {"sellers": Seller.objects.all()}
#     return render(request, 'all_users.html', context)


def show_sellers_for_current_game(request):
    """
    After a buyer selects a game, He will be shown a list of all those sellers
    who offers service for this game.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    game_name = request.POST.get("game")
    game = get_object_or_404(Game, name=game_name)
    game_clicked_signal.send(sender=None, game_object=game)
    game_sellers = SellerGame.objects.filter(game__name=game_name)
    context={"game_sellers": game_sellers}
    return render(request, 'game_sellers.html', context)


def show_games_for_current_seller(request):
    """
    After a buyer Chooses a Seller to buy his service, He will be shown a
    list of all those games which the selected Seller is offering service.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    name = request.POST.get("seller")
    seller = get_object_or_404(Seller, user__user_name=name)
    games = seller.seller_games.all()
    print(seller)
    context={"games": games, "seller": seller}
    return render(request, 'seller_games.html', context)


@login_required(login_url='accounts:login')
def show_all(request):
    """
    When a user selects a category type such as Games or Seller, He will be
    displayed list of all Games or Sellers depending on his selection
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    
    context={}
    text = ""
    if request.GET:
        choice = request.GET.get("choice")
        text = request.GET.get("search_text")    
        if choice=="Sellers": 
            context = {"sellers": Seller.objects.filter(user__user_name__icontains=text)}
            return render(request, 'all_users.html', context)
    context = {"games": Game.objects.filter(name__icontains=text)}
    return render(request, 'all_games.html', context)


def login_user(request):
    """
    If user is logged in then redirect him to Home page, else if user is
    autheticated then User is logged in but if authenction failed then error
    message is displayed. If User is superuser then redirect him
    to admin panel.
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





def display_profile(request, name):
    """
    It will display public profile of a given user with all public details.
    """
    # Seller.objects.annotate(total_orders = Count('orders')).aggregate(Avg('total_orders'))
    user = get_object_or_404(User, user_name=name)
    all_sellers_total_orders = Seller.objects.annotate(total_orders = Count('orders'))
    total_orders = all_sellers_total_orders.get(user=user).total_orders
    return render(request, "public_profile.html", {"user": user, "total_orders": total_orders})