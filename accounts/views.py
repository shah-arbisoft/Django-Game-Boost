"""Contains all the view fucntions."""

# pylint: disable=relative-beyond-top-level, no-member

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from games.models import Game, SellerGame
from games.signals import game_clicked_signal
from orders.models import Order

from accounts.models import Buyer, Seller, User

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
    signup_form = SignupForm()
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, 'Account Successfully Create')
            return redirect(reverse('accounts:login'))
    return render(request, 'signup.html', {'form': signup_form})


@login_required(login_url='accounts:login')
def home(request):
    """
    If User is logged-in then, if User is superuser then redirect him to
    Admin panel, else redirect him to Home page.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    Buyer.objects.get_or_create(user=request.user)
    return render(request, 'home.html')


def show_sellers_for_current_game(request):
    """
    After a buyer selects a game, A signal will be sent for the game he choosed
    and He will be shown a list of all those sellers who offers service for
    this game.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    game_name = request.POST.get("game")
    game = get_object_or_404(Game, name=game_name)
    game_clicked_signal.send(sender=None, game_object=game)
    game_sellers = (
        SellerGame.objects
        .filter(game__name=game_name)
        .select_related("seller")
    )
    context = {"game_sellers": game_sellers}
    return render(request, 'game_sellers.html', context)


def show_games_for_current_seller(request):
    """
    After a buyer Chooses a Seller to buy his service, He will be shown a
    list of all those games which the selected Seller is offering service for.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    name = request.POST.get("seller").lower()
    seller = get_object_or_404(Seller, user__user_name=name)
    games = seller.seller_games.select_related("game")
    context = {"games": games, "seller": seller}
    return render(request, 'seller_games.html', context)


@login_required(login_url='accounts:login')
def show_all(request):
    """
    When a user selects a category type such as Games or Seller, He will be
    displayed list of all Games or Sellers depending on his selection.
    """
    if request.user.is_superuser:
        return redirect('admin:login')

    context = {}
    text = ""
    if request.GET:
        choice = request.GET.get("choice")
        text = request.GET.get("search_text")
        if choice == "Sellers":
            context = {
                "sellers": Seller.objects
                .filter(user__user_name__icontains=text)
                .select_related("user")
            }
            return render(request, 'all_users.html', context)
    context = {
        "games": Game.objects.filter(name__icontains=text)
        .prefetch_related("categories")
    }
    return render(request, 'all_games.html', context)


def login_user(request):
    """
    If user is already logged in then redirect him to Home page, else if user is
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
    It will return rendered template 'profile.html' along with form intialized
    with about info whenever User wants to update his info.
    """
    form = ProfileUpdateForm()
    return render(request, "profile.html", {"form": form})


@login_required(login_url='accounts:login')
def update_user_profile(request):
    """
    To update User profile details, updated data is fetched from Form after a
    User makes a POST request and User profile is updated in Database with new
    Values. Any errors from Form validation fails will be shown.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            form.save(request=request)
        else:
            print(form.errors)
    return redirect("accounts:profile")


def display_profile(request, name):
    """
    It will display public profile of a given user with all user public details.
    """
    user = get_object_or_404(User, user_name=name)
    all_sellers_total_orders = Seller.objects.annotate(
        total_orders=Count('orders')
    )
    total_orders = all_sellers_total_orders.get(user=user).total_orders

    orders_of_seller = (
        user.seller.orders
        .values_list('id', flat=True)
        .order_by('buyer', 'order_start_time')
        .distinct('buyer')[:3]
    )
    recent_buyers = (
        Order.objects
        .filter(id__in=orders_of_seller)
        .order_by('-order_start_time')
        .values_list('buyer__user__user_name', flat=True)
    )
    return render(
        request,
        "public_profile.html",
        {
            "user": user,
            "total_orders": total_orders,
            "recent_buyers": recent_buyers
        }
    )
