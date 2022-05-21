"""All permissions for the api are defined here"""

from django.utils import timezone
from rest_framework import permissions


class HasCompletedOrderOrReadOnly(permissions.BasePermission):
    """
    Only allowed to make a read api call but if update or create api call is
    made then it ensures that a Buyer should only be allowed to give reviews
    for only those orders which Buyer has completed.
    """

    message = 'Current Buyer has not completed this order'

    def has_object_permission(self, request, view, obj):
        """
        Buyer will be allowed permission to give review if user who is
        giving review is buyer of this order and this order should be
        marked as completed.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        all_orders_buyer_has_completed = (
            request.user.buyer
            .orders
            .filter(status='cp')
            .values_list('id', flat=True)
        )
        return obj.id in all_orders_buyer_has_completed


class IsOrderRequirementsChangeableOrReadOnly(permissions.BasePermission):
    """
    Check if buyer is allowed to change requirements after certain time or not.
    """

    message = "Its too late, can not change requirements"

    def has_object_permission(self, request, view, obj):
        """
        Check if buyer is allowed to change requirements after certain time or not.

        Returns:
            bool: True if order is late and False if not late.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.buyer == request.user.buyer:
            due_time_for_changing_requirement = (
                obj.order_start_time
                + timezone.timedelta(
                    hours=obj.seller.time_limit_in_hours_for_changing_requirements
                )
            )
            if timezone.now() < due_time_for_changing_requirement:
                return True
        return False
