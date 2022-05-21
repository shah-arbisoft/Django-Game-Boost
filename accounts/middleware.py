from django.http.response import Http404
from django.shortcuts import redirect

from accounts.models import Seller


class DemoMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # print("hello brother")
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # print(f"function view name : {view_func.__name__}")
        if view_func.__name__ == "display_profile":
            username = view_kwargs.get("name")
            seller = Seller.objects.get(user__user_name=username)
            seller.clicks += 1
            seller.save()
            print("showing profile for " + username)
            print("total clicks  " , seller.clicks)


        # if view_func.__name__ == "show_sellers_for_current_game":
        #     if request.session.has_key("user_is"):
        #         if request.session["user_is"] != "buyer":
        #             redirect("accounts:home")