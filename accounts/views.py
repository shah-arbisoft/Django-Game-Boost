"""Contains all the view fucntions."""

# pylint: disable=relative-beyond-top-level, no-member

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.base import View
from games.models import Game

from accounts.models import Buyer, Seller

from .forms import ProfileUpdateForm, SignupForm


class SignupView(View):
    """
    To Create new Account, It first checks if USER is autheticated then
    redirect him to HOME page, If not then create SignupForm. And if request
    is a POST request then save the form after validating it, Account will be
    created and redirect user to Login Page.
    """

    form_class = SignupForm

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:home')

        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Successfully Create')
            return redirect(reverse('accounts:login'))
        return render(request, 'signup.html', {'form': form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        form = self.form_class()
        return render(request, 'signup.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class HomeView(generic.View):
    """
    If User is logged-in then, if User is superuser then redirect him to
    Admin panel, else redirect him to Home page.
    """
    def get(self, request):
        if request.user.is_superuser:
            return redirect('admin:login')
        return render(request, 'home.html')


class ShowGamesForCurrentSellerView(generic.DetailView):
    """
    After a buyer Chooses a Seller to buy his service, He will be shown a
    list of all those games which the selected Seller is offering service for.
    """
    model = Seller
    context_object_name = 'seller'
    template_name = "seller_games.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller_games = self.object.seller_games.select_related("game")
        context["seller_games"] = seller_games
        context["seller"] = self.object
        return context


@login_required(login_url='accounts:login')
def show_all(request):
    """
    When a user selects a category type such as Games or Seller, He will be
    displayed list of all Games or Sellers depending on his selection.
    """
    if request.user.is_superuser:
        return redirect('admin:login')

    Buyer.objects.get_or_create(user=request.user)
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


class LoginUserView(generic.View):
    """
    If user is already logged in then redirect him to Home page, else if user is
    autheticated then User is logged in but if authenction failed then error
    message is displayed. If User is superuser then redirect him
    to admin panel.
    """

    def post(self, request):
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

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        return render(request, 'login.html')


class LogoutView(generic.View):
    """
    It will Log out User and redirect him to Login page along success message.
    """
    def get(self, request):
        logout(request)
        messages.info(request, 'Log out successful')
        return redirect(reverse('accounts:login'))


class DisplayUserFormView(generic.FormView):
    """
    Display a form intialized with User Info with most of the fields editable
    so whenever User wants to update his info, he can.
    """
    form_class = ProfileUpdateForm
    template_name = "profile.html"


@method_decorator(login_required, name='dispatch')
class UpdateUserProfileView(generic.edit.FormView):
    """
    To update User profile details, updated data is fetched from Form after a
    User makes a POST request and User profile is updated in Database with new
    Values. Any errors from Form validation fails will be shown.
    """
    form_class = ProfileUpdateForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(request=request)
        else:
            messages.info(request, form.errors)
        return redirect("accounts:profile")

    def get(self, request):
        return redirect("accounts:profile")


class DisplayProfileDetailView(generic.DetailView):
    model = Seller
    context_object_name = "seller"
    template_name = "public_profile.html"
