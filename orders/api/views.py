"""Contains all the view fucntions for the API"""

from accounts.models import Seller
from games.models import Game
from orders.models import Order, Review
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

# pylint: disable=relative-beyond-top-level, no-member, invalid-name, unused-argument, no-self-use


from .permissions import (
    HasCompletedOrderOrReadOnly, IsOrderRequirementsChangeableOrReadOnly
)
from .serializers import (
    OrderRequirementsSerializer, OrderSerializer, RatingSerializer
)


@api_view(["GET"])
def api_overview(request):
    """
    Display all urls to which this API responds.
    """
    api_urls = {
        "List All Seller's ratings": "/api/rating/seller/",
        "View a Seller rating": "/api/rating/seller/<seller_id>/",
        "List all Games rating for a Seller": "/api/rating/seller/<seller_id>/game/",
        "View Game rating for Seller": "/rating/seller/<seller_id>/game/<game_id>/",
        "List All Game's ratings": "/api/rating/game/",
        "View a Game rating": "/api/rating/game/<game_id>/",
        "List all Seller's rating for a Game": "/api/rating/game/<game_id>/seller/",
        "View Seller rating for Game": "/rating/game/<game_id>/seller/<seller_id>/",
        "List Review of Order": "/api/review/order/",
        "Detail Review Order": "/api/review/order/<id>",
        "Update/Delete order requirement": "/api/order",
    }
    return Response(api_urls)


class SellerRatingList(ListAPIView):
    """Display ratings of all Sellers"""
    queryset = Seller.objects.all()
    serializer_class = RatingSerializer


class GameRatingList(ListAPIView):
    """Display ratings of all Games"""
    queryset = Game.objects.all()
    serializer_class = RatingSerializer


class SellerRating(RetrieveAPIView):
    """
    GET rating for a specific Seller based on "pk" of Seller.

    Args:
        pk (int): Primary key or ID of required Seller.

    Returns:
        (Json Fomat): Rating for requested Seller in Json format.
    """
    queryset = Seller.objects.all()
    serializer_class = RatingSerializer


class GameRating(RetrieveAPIView):
    """
    GET rating for a specific Game based on "pk" of Game.

    Args:
        pk (int): Primary key or ID of required Game.

    Returns:
        (Json Fomat): Rating for requested Game in Json format.
    """
    queryset = Game.objects.all()
    serializer_class = RatingSerializer


@api_view(["GET"])
def all_games_rating_for_given_seller(request, pk):
    """
    GET all game ratings for which current seller has offered his serices.

    Args:
        pk (int): Primary key or ID of required seller.

    Returns:
        (Json Fomat): Game_id, Game_rating of all games for this seller.
    """
    seller_games_review = Game.objects.filter(seller_games__seller=pk)
    serializer = RatingSerializer(seller_games_review, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def all_sellers_rating_for_given_game(request, pk):
    """
    GET all sellers rating who have offered services of this game.

    Args:
        pk (int): Primary key or ID of required game.

    Returns:
        (Json Fomat): Rating of all sellers for this game.
    """
    game_sellers_review = Seller.objects.filter(seller_games__game=pk)
    serializer = RatingSerializer(game_sellers_review, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def seller_rating_for_given_game(request, game_pk, seller_pk):
    """
    GET seller rating who have offered services of this game.

    Args:
        game_pk (int): Primary key or ID of required game.
        seller_pk (int): Primary key or ID of required Seller.


    Returns:
        (Json Fomat): Rating of seller for this game.
    """
    game_seller_review = Seller.objects.filter(
        seller_games__game=game_pk, id=seller_pk
    )
    serializer = RatingSerializer(game_seller_review, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def game_rating_for_given_seller(request, seller_pk, game_pk):
    """
    GET game rating offered as a service by this seller.

    Args:
        game_pk (int): Primary key or ID of required game.
        seller_pk (int): Primary key or ID of required seller.


    Returns:
        (Json Fomat): Rating of game for this seller.
    """
    seller_game_review = Game.objects.filter(
        id=game_pk, seller_games__seller=seller_pk
    )
    serializer = RatingSerializer(seller_game_review, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class OrderReviewList(APIView):
    """List all Order reviews, or create a new Order review."""

    permission_classes = [IsAuthenticatedOrReadOnly, HasCompletedOrderOrReadOnly]

    def get(self, request):
        """Get review of all Orders"""
        all_completed_orders_review = Review.objects.all()
        serializer = OrderSerializer(all_completed_orders_review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Replace if exists or Create a new review for an order but order should
        exists and should be of current buyer and should also be marked as
        completed.
        """
        try:
            order = Order.objects.get(id=request.data.get("order"))
        except Order.DoesNotExist:
            return Response("Order not found", status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, order)
        request.data["buyer"] = request.user.buyer.id
        try:
            review = Review.objects.get(order=order)
        except Review.DoesNotExist:
            review = Review.objects.create(
                order=order,
                rating=request.data.get("rating", 5),
                comment=request.data.get("comment", "")
            )
        serializer = OrderSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderReviewDetail(APIView):
    """Get, Update, Delete Review of an Order provided 'pk' of Order."""

    permission_classes = [IsAuthenticatedOrReadOnly, HasCompletedOrderOrReadOnly]

    def get_object(self, pk):
        """"
        Get Review object if exists of a completed Order.

        Args:
            pk (int): Primary key or ID of required Order.

        Returns:
            Review: Review Objects containing review of requested Order.
        """
        try:
            order = Order.objects.get(id=pk)
            try:
                return Review.objects.get(order=order)
            except Review.DoesNotExist:
                return None
        except Order.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        """Display review of requested Order"""
        review = self.get_object(pk)
        if not review:
            return Response("Object not found", status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(review, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """
        Update a review for an order but order should exists and should be of
        current buyer and should also be marked as completed.
        """
        review = self.get_object(pk)
        if not review:
            return Response("Object not found", status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete review of requested Order."""
        review = self.get_object(pk)
        if not review:
            return Response("Object not found", status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeOrderRequirements(APIView):
    """Update Order requirements or Delete an Order provided 'pk' of Order."""

    permission_classes = [
        IsAuthenticatedOrReadOnly, IsOrderRequirementsChangeableOrReadOnly
    ]

    def get_object(self, pk):
        """"
        Get requested Order requirements.

        Args:
            pk (int): Primary key or ID of required Order.

        Returns:
            Order: Requested Order will be returned.
        """
        try:
            return Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return None

    def patch(self, request, pk):
        """Update a requirements for an order"""
        order = self.get_object(pk)
        if not order:
            return Response("Order not found", status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, order)
        serializer = OrderRequirementsSerializer(
            instance=order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete requested Order."""
        order = self.get_object(pk)
        if not order:
            return Response("Order not found", status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, order)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
