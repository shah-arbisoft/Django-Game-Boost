"""This module contains all url paths for Accounts app"""

from django.urls import path

# pylint: disable=relative-beyond-top-level, invalid-name
from . import views

app_name = "accounts"
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.DisplayUserFormView.as_view(), name='profile'),
    path('list/', views.show_all, name='show_all'),
    path('update_profile/', views.UpdateUserProfileView.as_view(), name='update_profile'),
    path(
        'seller/<int:pk>/games',
        views.ShowGamesForCurrentSellerView.as_view(),
        name='show_games_for_current_seller'
    ),
    path('<int:pk>/', views.DisplayProfileDetailView.as_view(), name='display_profile'),
]
