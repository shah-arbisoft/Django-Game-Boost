"""
This module contains all models defining Games, Review and User
relation with Game.
"""

# pylint: disable=no-member, invalid-str-returned

from accounts.models import FIVE_STAR, Seller
from django.db import models
from django.db.models.fields.related import ForeignKey


class Category(models.Model):
    """
    All Games will lies in one or many of the categories therefore every
    Game object will be linked to atleast one of the object of this model.
    """
    name = models.CharField("Categories", max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    """
    This model will handle all the listed games and will retain information of
    each game such as name and image of a given game.
    """
    image = models.ImageField(null=True, blank=True)
    name = models.CharField("Name of game", max_length=100)
    description = models.TextField("Description of Game", blank=True, default="")
    categories = models.ManyToManyField(Category, related_name="games")
    rating = models.FloatField("Rating", default=FIVE_STAR)
    clicks = models.PositiveIntegerField("Number of clicks recieved", default=0)

    class Meta:
        ordering = ["-rating"]

    def __str__(self):
        return self.name


class SellerGame(models.Model):
    """
    It will hold relation information between Seller model and Game model for
    which he offer service.
    """
    game = ForeignKey(
        Game, related_name="seller_games", on_delete=models.CASCADE
    )

    seller = ForeignKey(
        Seller, related_name="seller_games", on_delete=models.CASCADE
    )
    seller_price = models.PositiveIntegerField("Price", null=True, blank=True)
    seller_description_of_game = models.TextField(
        "Seller description of Game", blank=True, null=True
    )

    def __str__(self):
        return f"{self.id}"
