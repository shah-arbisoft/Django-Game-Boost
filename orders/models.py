import datetime

from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.utils import timezone
from django.utils.translation import gettext as _

from accounts.models import Buyer, Seller
from games.models import Game


class Order(models.Model):
    # title 
    class Status(models.TextChoices):
        ACTIVE = "at", "Active"
        COMPLETED = "cp", "Completed"
        DELIVERED = "dl", "Delivered"
        CANCELED = "cd", "Canceled"
   

    buyer = ForeignKey(Buyer, related_name="orders", on_delete=models.CASCADE)
    seller = ForeignKey(Seller, related_name="orders", on_delete=models.CASCADE)
    gaming_account_id = models.CharField(verbose_name=_("Your Gaming Accound ID"), max_length=100)
    gaming_account_password = models.CharField(verbose_name=_("Password"), max_length=50)
    price = models.PositiveIntegerField(null=False)
    game = models.ForeignKey(Game, related_name="orders", verbose_name=_("Select Game"), on_delete=models.CASCADE)
    description = models.TextField(verbose_name=_("Description"), max_length=999, blank=True)
    order_start_time = models.DateTimeField(auto_now_add=True)
    number_of_days_for_completing_the_order = models.PositiveIntegerField(null=False, blank=False)
    status = models.CharField(verbose_name=_("Status"), max_length=2, choices=Status.choices)

    @property
    def get_remaining_time_for_order_delivery(self):
        """
        It will calcuate the remaining time from today to due time of order delivery
        """
        time_lapsed = (
            datetime.timedelta(days=self.number_of_days_for_completing_the_order)
            + self.order_start_time
        )
        return time_lapsed - timezone.now()
       
    def __str__(self):
        return f"{self.seller}-{self.buyer}-{self.game}"