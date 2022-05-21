# from games.models import Game, SellerGame
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.db.models import Min
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,                                         
    OneToOneField
)
from django.utils import timezone

FIVE_STAR = 5

class AccountManager(BaseUserManager):

    def create_user(
        self, email, user_name, first_name, password, **other_fields
    ):
        email = self.normalize_email(email)
        if not email:
            raise ValueError('You must provide an email address')
        if not user_name:
            raise ValueError('You must provide an username')
        user = self.model(
            email=email, user_name=user_name, first_name=first_name, **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email, user_name, first_name, password, **otherfields
    ):
        otherfields.setdefault('is_staff', True)
        otherfields.setdefault('is_superuser', True)
        otherfields.setdefault('is_active', True)
        if otherfields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True'
            )
        if otherfields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True'
            )
        return self.create_user(
            email, user_name, first_name, password, **otherfields
        )


def default_profile_image():
    """Default profile image to be used for every user if he have not set any."""
    return 'avatar.png'


def get_profile_image_filepath(self, filename):
    """
    When User set his profile image, the uploaded imaged will be saved in
    a folder named as User primary key and withing will be the uploaded image.
    """
    return f'{self.pk}/{filename}'


def get_age_from_date_of_birth(date_of_birth):
    """
    When User sets his date of birth, his age will be automatically calculated
    and returned.

    Returns:
        (int): Total age of User as of today
    """
    age_as_of_today =  timezone.now() - date_of_birth
    age_in_years = (age_as_of_today.days/30)/12
    return age_in_years


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email address', unique=True)
    user_name = models.CharField('User name', max_length=50, unique=True)
    full_name = models.CharField("Full name", max_length=50, blank=True)
    joining_date = models.DateTimeField("Date of joining", auto_now_add=True)
    age = models.PositiveIntegerField("Age", null=True, blank=True)
    date_of_birth = models.DateTimeField("Date of birth", blank=True, null=True)
    about_info = models.TextField("About info", max_length=500, blank=True)
    cnic = models.CharField("CNIC number", max_length=15, default="XXXXX-XXXXXXX-X", blank=True)
    credit_card_number = models.CharField("Credit card number", max_length=24, blank=True)
    profile_image = models.ImageField(
        max_length=255, null=True, blank=True,
        upload_to=get_profile_image_filepath, default=default_profile_image
    )
    hide_email = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    objects = AccountManager()

    def __str__(self):
        return self.user_name

    def save(self, *args, **kwargs):
        """Update Age automatically from Date of birth on save method call"""
        if self.date_of_birth:
            self.age = int(get_age_from_date_of_birth(self.date_of_birth))
        super(User, self).save(*args, **kwargs)


class Seller(models.Model):
    class BadgeRanks(models.IntegerChoices):
        BRONZE = 0, 'Bronze'
        SILVER = 1, 'Silver'
        GOLD = 2, 'Gold'
        MASTER = 3, 'Master'

    rating = models.FloatField("Rating", default=FIVE_STAR)
    total_number_of_completed_orders = 0
    user = OneToOneField(User, related_name='seller', on_delete=models.CASCADE)
    clicks = models.PositiveBigIntegerField("profile visits", default=0)
    rank_badge = models.IntegerField(
        choices=BadgeRanks.choices,
        default=BadgeRanks.BRONZE,
    )

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return self.user.user_name

    @property
    def starting_price(self):
        """
        It will calculate price of every game the Seller is offering service for,
        and return the minimum price among all his games

        Returns:
            (int): Price of his cheapest game he is offering.
        """
        prices = Seller.objects.filter(user=self.user).aggregate(min_price=Min('seller_games__seller_price'))
        return prices.get("min_price")


class Buyer(models.Model):
    user = OneToOneField(User, related_name='buyer', on_delete=models.CASCADE)    
    total_number_of_completed_orders = 0

    def __str__(self):
        return self.user.user_name


class Review(models.Model):
    seller = models.ForeignKey(Seller, related_name="reviews", on_delete=models.CASCADE)
    rating = models.FloatField("Rating", default=FIVE_STAR)
    comment = models.TextField("Review Comment", max_length=500, blank=True, null=True)

    