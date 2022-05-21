"""Contains all the view fucntions for model Game."""

# pylint: disable=relative-beyond-top-level, no-member
from accounts.models import Seller
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from games.signals import game_clicked_signal

from .forms import AddGameForm
from .models import Game, SellerGame


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


def show_sellers_for_current_game(request, game_pk):
    """
    After a buyer selects a game, A signal will be sent for the game he choosed
    and He will be shown a list of all those sellers who offers service for
    this game.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    game = get_object_or_404(Game, id=game_pk)
    game_clicked_signal.send(sender=None, game_object=game)
    game_sellers = (
        SellerGame.objects
        .filter(game=game)
        .select_related("seller")
    )
    context = {"game_sellers": game_sellers}
    return render(request, 'game_sellers.html', context)


def show_all_games_for_which_seller_offer_service(request):
    """
    If current authenticated User is acting as a Seller and wants to display
    all the games for which he is offering services, those will be displayed.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    seller, _ = Seller.objects.get_or_create(user=request.user)
    seller_games = seller.seller_games
    if seller_games:
        seller_games = seller_games.all()
    context = {"games": seller_games}
    return render(request, 'my_games.html', context)


def display_form_to_add_game_to_seller(request):
    """
    If a seller wants to add a game to list of games for which he offers
    services, He will fill and submit this form will all the details and
    that game will be added.
    """
    if request.method == 'POST':
        form = AddGameForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Game added successfully')
            return redirect(reverse("games:my_games"))
    form = AddGameForm(initial={'seller': request.user.seller})
    return render(request, 'seller_add_game.html', {'form': form})
