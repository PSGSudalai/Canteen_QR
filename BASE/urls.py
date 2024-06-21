from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
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
    qr_scan_view,
    PreviousOrdersListView,
    TransactionListView,
    student_list,
    staff_list,
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
    path("canteen/qr_scan/", qr_scan_view, name="qr_scan"),
    path(
        "previous-orders/",
        PreviousOrdersListView.as_view(),
        name="previous_orders_list",
    ),
    path("transactions/", TransactionListView.as_view(), name="transaction_list"),
    path("staff_list/", staff_list, name="staff_list"),
    path("student_list/", student_list, name="student_list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
