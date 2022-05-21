"""Contains all the view fucntions."""

# pylint: disable=relative-beyond-top-level
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.edit import FormView

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
    context = {"games": Game.objects.all()}
    return render(request, 'all_games.html', context)


def all_games_for_which_seller_offer_service(request):
    """
    If current authenticated User is acting as a Seller wants to display
    all the games for which he is offering services, this function will do it.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    seller_games = request.user.seller.seller_games
    if seller_games:
        seller_games = seller_games.all()    
    context = {"games": seller_games, "seller":True}
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
            return redirect(reverse("games:my_games"))
    form = AddGame(initial={'seller': request.user.seller})
    return render(request, 'seller_add_game.html', {'form': form})
