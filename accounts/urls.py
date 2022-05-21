from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.get_user_profile_details, name='profile'),
    path('list/', views.show_all, name='show_all'),
    path('update_profile/', views.update_user_profile, name='update_profile'),
    path('game_sellers/', views.show_sellers_for_current_game, name='show_sellers_for_current_game'),
    path('seller_games/', views.show_games_for_current_seller, name='show_games_for_current_seller'),
    path('<str:name>/', views.display_profile, name='display_profile'),

    
]
