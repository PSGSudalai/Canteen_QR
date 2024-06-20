from django.urls import path
from BASE.views import (
    signup_view,
    login_view,
    logout_view,
    canteen_item_list,
    canteen_item_create,
    add_to_cart,
    clear_cart_items,
    CartListView,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("canteen/items/", canteen_item_list, name="canteen_item_list"),
    path("canteen/items/create/", canteen_item_create, name="canteen_item_create"),
    path("cart/add/", add_to_cart, name="add_to_cart"),
    path("cart/clear/", clear_cart_items, name="clear_cart_items"),
    path("cart/", CartListView.as_view(), name="cart_list"),
]
