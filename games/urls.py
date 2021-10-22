"""URL Configuration for Game app"""

from django.urls import path

# pylint: disable=relative-beyond-top-level, invalid-name
from . import views

app_name = "games"

urlpatterns = [
    path(
        'all_games/',
        views.show_all_games,
        name='all_games'
    ),
    path(
        'seller_games/',
        views.all_games_for_which_seller_offer_service,
        name='my_games'
    ),
    path(
        'add_game/',
        views.add_game_to_seller,
        name='add_game'
    ),
]
