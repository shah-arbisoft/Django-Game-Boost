from django.db import models



class Category(models.Model):
    name = models.CharField("Category", max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    image = models.ImageField(null=True, blank=True)
    dummy = models.CharField(max_length=5, default="3")
    name = models.CharField("Name of game", max_length=100, null=True)
    description = models.TextField("Description of Game", blank=True)
    category = models.ManyToManyField(Category, related_name="category")

    
    def __str__(self):
        return self.name



