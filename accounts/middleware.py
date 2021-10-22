"""This contains all custom middlewares for Accounts app"""

# pylint: disable=unused-argument, no-self-use, no-member
from accounts.models import Seller


class ProfileClicksMiddleWare:
    """Custom midddleware to increment profile clicks."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Whenever Seller profile is clicked or viewed, view function
        "display_profile" is called, Seller clicks are incremented by 1.
        """
        if view_func.__name__ == "display_profile":
            username = view_kwargs.get("name")
            try:
                seller = Seller.objects.get(user__user_name=username)
                seller.clicks += 1
                seller.save()
            except Seller.DoesNotExist:
                pass
