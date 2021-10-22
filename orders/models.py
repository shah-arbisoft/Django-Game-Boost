"""
This module contains model defining Order and defines what informations Order
contain and what it can do with it.
"""

# pylint: disable=no-member

import datetime

from accounts.models import FIVE_STAR, Buyer, Seller
from django.db import models
from django.db.models.aggregates import Avg
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.utils.translation import gettext as _
from games.models import Game


class Order(models.Model):
    """
    User model defining a  USER by its attributes and methods.
    """

    class Status(models.TextChoices):
        """Contains Choices available for Order Status"""
        ACTIVE = "at", "Active"
        COMPLETED = "cp", "Completed"
        DELIVERED = "dl", "Delivered"
        CANCELED = "cd", "Canceled"
        LATE = "lt", "Late"

    buyer = ForeignKey(Buyer, related_name="orders", on_delete=models.CASCADE)
    seller = ForeignKey(Seller, related_name="orders", on_delete=models.CASCADE)

    gaming_account_id = models.CharField(
        verbose_name=_("Your Gaming Accound ID"), max_length=100
    )
    gaming_account_password = models.CharField(
        verbose_name=_("Password"), max_length=50
    )
    game = models.ForeignKey(
        Game,
        related_name="orders",
        verbose_name=_("Select Game"),
        on_delete=models.CASCADE
    )

    order_start_time = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField(null=False)
    description = models.TextField(
        verbose_name=_("Description"), max_length=999, blank=True
    )
    number_of_days_for_completing_the_order = models.PositiveIntegerField(
        null=False, blank=False
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=2,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    @property
    def get_remaining_time_for_order_delivery(self):
        """
        It will calcuate that how much time remains till order delivery
        date as of today.

        Returns:
            datetime.timedelta: Will return positive time in days/seconds
                remaining till order delivery date if order is not late, else
                it will contain negtive time since order due date has passed.
        """
        time_lapsed = (
            datetime.timedelta(days=self.number_of_days_for_completing_the_order)
            + self.order_start_time
        )
        return time_lapsed - timezone.now()

    @property
    def is_order_late(self):
        """
        It will check if orders due date has passed or not.

        Returns:
            bool: True if order is late and False if not late.
        """
        if datetime.timedelta(0) > self.get_remaining_time_for_order_delivery:
            return True
        return False

    def __str__(self):
        return f"{self.id}_{self.status}"


class Review(models.Model):
    """
    This class defines a Review and relation formed based on review of buyer,
    seller and Order with eachother.
    """
    order = ForeignKey(
        Order, related_name="review", on_delete=models.CASCADE, null=True
    )
    comment = models.TextField(
        "Review Comment", max_length=500, blank=True, default=""
    )
    rating = models.FloatField("Rating", default=FIVE_STAR)

    def _update_rating_of_seller_of_this_order(self):
        """
        Get all orders rating for seller of this order, find average and set it
        as this seller overall rating.
        """
        average_rating_of_current_seller = (
            Seller.objects
            .filter(id=self.order.seller.id)
            .aggregate(avg_rating=Avg("orders__review__rating"))
        )
        average_rating_of_current_seller = average_rating_of_current_seller.get(
            'avg_rating'
        )
        if average_rating_of_current_seller:
            self.order.seller.rating = average_rating_of_current_seller
        else:
            self.order.seller.rating = self.rating
        self.order.seller.save()

    def _update_rating_of_game_of_this_order(self):
        """
        Get all orders rating for game of this order, find average and set it
        as this game overall rating.
        """
        average_rating_of_current_game = (
            Game.objects
            .filter(id=self.order.game.id)
            .aggregate(avg_rating=Avg("orders__review__rating"))
        )
        average_rating_of_current_game = average_rating_of_current_game.get(
            'avg_rating'
        )
        if average_rating_of_current_game:
            self.order.game.rating = average_rating_of_current_game
        else:
            self.order.game.rating = self.rating
        self.order.game.save()

    def save(self, *args, **kwargs):
        """
        After saving review for current order, All review ratings of orders
        for game and seller of this order
        """
        super().save(*args, **kwargs)
        self._update_rating_of_game_of_this_order()
        self._update_rating_of_seller_of_this_order()
