"""URL Configuration for Game app"""

from django.urls import path

# pylint: disable=relative-beyond-top-level, invalid-name
from . import views

app_name = "orders"
urlpatterns = [
    path(
        '',
        views.api_overview,
        name='api_overview'
    ),

    path(
        'rating/seller/',
        views.SellerRatingList.as_view(),
        # name='all_seller_review'
        name='all_seller_ratings'
    ),

    path(
        'rating/game/',
        views.GameRatingList.as_view(),
        # name='all_games_review_for_given_seller'
        name='all_game_ratings'
    ),

    path(
        'rating/seller/<int:pk>/',
        views.SellerRating.as_view(),
        name='seller_rating'
    ),

    path(
        'rating/game/<int:pk>/',
        views.GameRating.as_view(),
        name='game_rating'
    ),

    path(
        'rating/seller/<int:pk>/game/',
        views.all_games_rating_for_given_seller,
        name='all_games_rating_for_given_seller'
    ),

    path(
        'rating/game/<int:pk>/seller/',
        views.all_sellers_rating_for_given_game,
        name='all_sellers_rating_for_given_game'
    ),

    path(
        'rating/seller/<int:seller_pk>/game/<int:game_pk>',
        views.game_rating_for_given_seller,
        name='game_rating_for_given_seller'
    ),

    path(
        'rating/game/<int:game_pk>/seller/<int:seller_pk>',
        views.seller_rating_for_given_game,
        name='seller_rating_for_given_game'
    ),

    path(
        'review/order/',
        views.OrderReviewList.as_view(),
        name='all_orders_review'
    ),
    path(
        'review/order/<int:pk>/',
        views.OrderReviewDetail.as_view(),
        name='detail_order_review'
    ),

    path(
        'order/<int:pk>/',
        views.ChangeOrderRequirements.as_view(),
        name='update_order_requirements'
    ),



]
