"""
This module contains view methods related to Order model
"""

from accounts.models import Seller
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from games.models import Game, SellerGame

# pylint: disable=relative-beyond-top-level
from .forms import PlaceOrderForm


def create_order(request, seller_game):
    """
    When a user wants to start an order, when makes GET request,
    PlacingOrder form will be displayed to him by directing him to
    template:create_order.html. When he make a POST request after submiting
    FORM, if FORM is valid then starts an order by creating an Order object.
    """
    if request.method == 'POST':
        form = PlaceOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order Successfully Created')
            return redirect(reverse('accounts:home'))

    seller_game_obj = get_object_or_404(SellerGame, id=seller_game)
    seller = get_object_or_404(Seller, id=seller_game_obj.seller.id)
    game = get_object_or_404(Game, id=seller_game_obj.game.id)

    form = PlaceOrderForm(
        initial={
            "buyer": request.user.buyer.id,
            "seller": seller.id,
            "game": game.id
        }
    )

    return render(
        request,
        "create_order.html",
        {
            "form": form,
            "seller": seller,
            "game": game,
            "buyer": request.user
        }
    )


def show_all_orders_of_current_user(request):
    """
    If user is logged in then redirect him to Admin page else show him his
    Orders inlcuded Active, Completed and Cancelled.
    """
    if request.user.is_superuser:
        return redirect('admin:login')
    context = {
        "orders": request.user.buyer.orders.select_related("game")
    }
    return render(request, 'my_orders.html', context)
