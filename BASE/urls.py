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
    canteen_item_edit,
    canteen_item_archive,
    add_to_cart,
    update_cart_item,
    clear_cart_items,
    delete_cart_item,
    CartListView,
    balance_check_view,
    qr_image_view,
    qr_scan_recharge_view,
    qr_scan_payment_view,
    PreviousOrdersListView,
    TransactionListView,
    student_list,
    staff_list,
    edit_user,
    recharge_transaction,
    payment_transaction,
    archive_user,
    archived_student_list,
    unarchive_user,
    archived_items_list_view,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("qr_image/<int:user_id>/", qr_image_view, name="qr_image"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("students/archive/<int:id>/", archive_user, name="archive_user"),
    path("students/unarchive/<int:id>/", unarchive_user, name="unarchive_user"),
    path("students/archived/", archived_student_list, name="archived_student_list"),
    path("canteen/items/", canteen_item_list, name="canteen_item_list"),
    path("canteen/items/create/", canteen_item_create, name="canteen_item_create"),
    path("items/edit/<int:item_id>/", canteen_item_edit, name="canteen_item_edit"),
    path(
        "items/archive/<int:item_id>/",
        canteen_item_archive,
        name="canteen_item_archive",
    ),
    path("cart/add/", add_to_cart, name="add_to_cart"),
    path("update-cart-item/<int:item_id>/", update_cart_item, name="update_cart_item"),
    path("clear_cart/", clear_cart_items, name="clear_cart"),
    path("balance_check/", balance_check_view, name="balance_check"),
    path("delete_cart_item/<int:item_id>/", delete_cart_item, name="delete_cart_item"),
    path("cart/", CartListView.as_view(), name="cart_list"),
    path("canteen/qr_scan_recharge/", qr_scan_recharge_view, name="qr_scan_recharge"),
    path("canteen/qr_scan_payment/", qr_scan_payment_view, name="qr_scan_payment"),
    path(
        "previous-orders/",
        PreviousOrdersListView.as_view(),
        name="previous_orders_list",
    ),
    path("transactions/", TransactionListView.as_view(), name="transaction_list"),
    path("staff_list/", staff_list, name="staff_list"),
    path("student_list/", student_list, name="student_list"),
    path("edit-user/<int:user_id>/", edit_user, name="edit_user"),
    path("recharge/<uuid>/", recharge_transaction, name="recharge_transaction"),
    path("payment/<uuid>/", payment_transaction, name="payment_transaction"),
    path("archived-items/", archived_items_list_view, name="archived_items_list"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
