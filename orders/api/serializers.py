"""All custom serialzers are defined here"""

# pylint: disable=too-few-public-methods
from orders.models import Order, Review
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    """To Serialize review for a completed Order"""
    class Meta:
        """Changing default Serializer behaviour"""
        model = Review
        fields = '__all__'


class OrderRequirementsSerializer(serializers.ModelSerializer):
    """To Serialize Order requirements"""

    class Meta:
        """Changing default Serializer behaviour"""

        model = Order
        fields = [
            'price',
            'gaming_account_id',
            "gaming_account_password",
            "game",
            "description",
            "number_of_days_for_completing_the_order"
        ]


class RatingSerializer(serializers.ModelSerializer):
    """To Serialize rating for requested object"""
    class Meta:
        """Changing default Serializer behaviour"""
        model = Review
        fields = ['id', 'rating']
