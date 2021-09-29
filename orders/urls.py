from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    # path('<int:id>', views.create_order, {}, name='creating_order'),
    path('<int:id>', views.create_order, {}, name='creating_order'),
]
