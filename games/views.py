"""Contains all the view fucntions for model Game."""

# pylint: disable=relative-beyond-top-level, no-member
from accounts.models import Seller
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import AddGame
from .models import Game


@login_required(login_url='accounts:login')
def show_all_games(request):
    """
    If user is logged in then redirect him to Admin page else show him all
    the Games currently available to buy.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    context = {"games": Game.objects.prefetch_related("categories")}
    return render(request, 'all_games.html', context)


def all_games_for_which_seller_offer_service(request):
    """
    If current authenticated User is acting as a Seller and wants to display
    all the games for which he is offering services, this function will do it.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    seller, _ = Seller.objects.get_or_create(user=request.user)
    seller_games = seller.seller_games
    if seller_games:
        seller_games = seller_games.all()
    context = {"games": seller_games}
    return render(request, 'my_games.html', context)


def add_game_to_seller(request):
    """
    If a seller wants to add a game to list of games for which he offers
    services, He will fill and submit this form will all the details and
    that game will be added.
    """
    if request.method == 'POST':
        form = AddGame(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Game added successfully')
            return redirect(reverse("games:my_games"))
    form = AddGame(initial={'seller': request.user.seller})
    return render(request, 'seller_add_game.html', {'form': form})
