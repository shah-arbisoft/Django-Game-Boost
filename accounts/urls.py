from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.get_user_profile_details, name='profile'),
    path('update_profile/', views.update_user_profile, name='update_profile'),
]
