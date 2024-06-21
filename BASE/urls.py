from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from BASE.views import (
    signup_view,
    login_view,
    logout_view,
    canteen_item_list,
    canteen_item_create,
    add_to_cart,
    clear_cart_items,
    delete_cart_item,
    CartListView,
    qr_image_view,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("qr_image/", qr_image_view, name="qr_image"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("canteen/items/", canteen_item_list, name="canteen_item_list"),
    path("canteen/items/create/", canteen_item_create, name="canteen_item_create"),
    path("cart/add/", add_to_cart, name="add_to_cart"),
    path("clear_cart/", clear_cart_items, name="clear_cart"),
    path("delete_cart_item/<int:item_id>/", delete_cart_item, name="delete_cart_item"),
    path("cart/", CartListView.as_view(), name="cart_list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
