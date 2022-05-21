from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField

from accounts.models import Seller


class Category(models.Model):
    """
    All Games will lies in one or many of the categories therefore every
    Game object will be linked to atleast one of the object of this model.
    """
    name = models.CharField("Category", max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    """
    This model will handle all the listed games and will retain information of
    each game such as name and image of a given game.
    """
    image = models.ImageField(null=True, blank=True)
    name = models.CharField("Name of game", max_length=100, null=True)
    description = models.TextField("Description of Game", blank=True)
    categories = models.ManyToManyField(Category, related_name="games")
    clicks = models.PositiveIntegerField("Number of clicks recieved", default=0)
    
    def __str__(self):
        return self.name


class SellerGame(models.Model):
    """
    It will hold relation information between Seller and A Game for 
    which he offer service.
    """
    game = ForeignKey(Game, related_name="seller_game", on_delete=models.CASCADE)
    seller = ForeignKey(Seller, related_name="seller_games", on_delete=models.CASCADE, null=True)
    seller_price = models.PositiveIntegerField("Price", null=True, blank=True)
    seller_description_of_game = models.TextField("Seller description of Game", blank=True, null=True)

    def __str__(self):
        return self.game.name




