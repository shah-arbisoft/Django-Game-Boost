"""
This module contains all models defining our user when behaving
as a seller, buyer etc.
"""

import orders
# pylint: disable=no-member, too-few-public-methods
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.db.models import Min
from django.db.models.aggregates import Count
from django.db.models.fields.related import OneToOneField

from .constants import FIVE_STAR
from .helpers import get_age_from_date_of_birth


class AccountManager(BaseUserManager):
    """
    Custom Manager defined for creating a regular and super user.
    """
    def create_user(
        self, email, user_name, first_name, password, **other_fields
    ):
        """
        To create a user by a custom manager.

        Args:
            email (str): email of user which will be unique
            user_name (str): user name of user which is also unique for
                every user
            first_name (str): First name of user
            password (str): Password to be used for future login actions.

        Returns:
            user : Returns created object of user with passed details after
                 creating it.
        """
        email = self.normalize_email(email)
        if not email:
            raise ValueError('You must provide an email address')
        if not user_name:
            raise ValueError('You must provide an username')
        user = self.model(
            email=email,
            user_name=user_name,
            first_name=first_name,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email, user_name, first_name, password, **otherfields
    ):
        """
        To create a super user by a custom manager.

        Args:
            email (str): email of super user which will be unique
            user_name (str): user name of super user which is also
                unique for every user
            first_name (str): First name of super user
            password (str): Password to be used for future login actions.

        Returns:
            user : Returns created object of super user after creating it.
        """
        otherfields.setdefault("is_staff", True)
        otherfields.setdefault("is_superuser", True)
        otherfields.setdefault("is_active", True)
        if otherfields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must be assigned to is_staff=True"
            )
        if otherfields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True"
            )
        return self.create_user(
            email, user_name, first_name, password, **otherfields
        )


def default_profile_image():
    """Default profile image to be used for every user if he have not set any."""
    return "avatar.png"


def get_profile_image_filepath(self, filename):
    """
    When User set his profile image, the uploaded imaged will be saved in
    a folder named as User primary key and within will be the uploaded image.
    """
    return f"{self.pk}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model defining a USER by it's attributes and methods.
    """
    email = models.EmailField("Email address", unique=True)
    password = models.CharField(max_length=100)
    user_name = models.CharField("User name", max_length=50, unique=True)
    full_name = models.CharField("Full name", max_length=50, blank=True)
    joining_date = models.DateTimeField("Date of joining", auto_now_add=True)
    age = models.PositiveIntegerField("Age", null=True, blank=True)
    date_of_birth = models.DateTimeField("Date of birth", blank=True, null=True)
    about_info = models.TextField("About info", max_length=500, blank=True)

    cnic = models.CharField(
        "CNIC number", max_length=15, default="XXXXX-XXXXXXX-X", blank=True
    )
    credit_card_number = models.CharField(
        "Credit card number", max_length=24, blank=True
    )
    profile_image = models.ImageField(
        max_length=255, blank=True,
        upload_to=get_profile_image_filepath, default="avatar.png"
    )

    hide_email = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name", "first_name"]

    objects = AccountManager()

    def save(self, *args, **kwargs):
        """Update Age automatically from Date of birth on save method call"""
        if self.date_of_birth:
            self.age = get_age_from_date_of_birth(self.date_of_birth)
        super().save(*args, **kwargs)


class UserCommonInfo(models.Model):
    """Abstract model to contain common info for Buyer and Seller."""
    total_number_of_completed_orders = 0

    def __str__(self):
        """String representation of Object"""
        return f"{self.id}"

    class Meta:
        abstract = True


class Seller(UserCommonInfo):
    """Model to define a Seller."""

    class BadgeRanks(models.IntegerChoices):
        """Contains Choices available for badge ranks"""
        BRONZE = 0, "Bronze"
        SILVER = 1, "Silver"
        GOLD = 2, "Gold"
        MASTER = 3, "Master"

    user = OneToOneField(User, related_name="seller", on_delete=models.CASCADE)
    rating = models.FloatField("Rating", default=FIVE_STAR)
    clicks = models.PositiveBigIntegerField("profile visits", default=0)
    providing_services_to_number_of_games = models.PositiveIntegerField(
        "Number of Games", default=0, blank=True
    )

    time_limit_in_hours_for_changing_requirements = \
        models.PositiveBigIntegerField(default=8)

    rank_badge = models.IntegerField(
        choices=BadgeRanks.choices,
        default=BadgeRanks.BRONZE,
    )

    class Meta:
        ordering = ["-rating", "-providing_services_to_number_of_games"]

    def save(self, *args, **kwargs):
        """
        Saving and updating the field 'providing_services_to_number_of_games'.
        """
        self.providing_services_to_number_of_games = self.seller_games.count()
        super().save(*args, **kwargs)

    @property
    def starting_price(self):
        """
        Calculate price of every game the Seller is offering service for,
        and return the minimum price among all his games

        Returns:
            (int): Price of his cheapest game he is offering.
        """
        prices = Seller.objects.filter(user=self.user).aggregate(
            min_price=Min("seller_games__seller_price")
        )
        return prices.get("min_price")

    @property
    def total_number_of_orders(self):
        """
        Calculate total of number of orders this seller has completed
        or cuurently ongoing.

        Returns:
            (int): Total number of orders of this seller.
        """
        all_sellers_total_orders = Seller.objects.annotate(
            total_orders=Count('orders')
        )
        return all_sellers_total_orders.get(user=self.user).total_orders

    @property
    def recent_buyers(self):
        """
        Returns 3 recent buyers of this seller.

        Returns:
            (int): Last 3 unique buyers who initiated order with this seller.
        """
        orders_of_seller = (
            self.orders
            .values_list('id', flat=True)
            .order_by('buyer', 'order_start_time')
            .distinct('buyer')[:3]
        )
        recent_buyers = (
            orders.models.Order.objects
            .filter(id__in=orders_of_seller)
            .order_by('-order_start_time')
            .values_list('buyer__user__user_name', flat=True)
        )
        return recent_buyers


class Buyer(UserCommonInfo):
    """Model to define a Buyer."""

    user = OneToOneField(User, related_name="buyer", on_delete=models.CASCADE)
