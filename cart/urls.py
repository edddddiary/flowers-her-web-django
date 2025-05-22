from django.urls import path
from . import views 

app_name="cart"

urlpatterns = [
    path("remove_cart/<int:product_id>/<int:cart_item_id>/", views.remove_cart, name ="remove_cart"),
    path("increment/<int:product_id>", views.add_cart, name ="increment"),
    path("decrement/<int:product_id>/<int:cart_item_id>/", views.decrement, name ="decrement"),
    path("add_cart/<int:product_id>/", views.add_cart, name="add_cart"),
    path("", views.index, name="index"),
]
