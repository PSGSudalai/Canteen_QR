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
    archive_staff,
    archived_student_list,
    archived_staff_list,
    unarchive_staff,
    unarchive_user,
    archived_items_list_view,
    generate_payment_report_all,
    canteen_item_unarchive,
    redirect_transaction_report_page,
    redirect_sales_report_page,
    generate_product_sales_day_based_report_all,
    generate_product_sales_month_based_report_all,
    generate_product_sales_report_all,
    delete_staff,
    delete_user,
    canteen_delete_item,
    cancel_transaction,
    custom_404_view,
)

#  custom page for error handling
handler404 = custom_404_view

urlpatterns = [
    # User Creation
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # user function
    path("qr_image/<uuid>/", qr_image_view, name="qr_image"),
    path("balance_check/", balance_check_view, name="balance_check"),
    # user
    path("student_list/", student_list, name="student_list"),
    path("edit-user/<uuid>/", edit_user, name="edit_user"),
    path("students/archive/<int:id>/", archive_user, name="archive_user"),
    path("students/unarchive/<int:id>/", unarchive_user, name="unarchive_user"),
    path("student/delete/<int:id>/", delete_user, name="delete_user"),
    path("students/archived/", archived_student_list, name="archived_student_list"),
    # staff
    path("staff_list/", staff_list, name="staff_list"),
    path("staff/archive/<int:id>/", archive_staff, name="archive_staff"),
    path("staff/unarchive/<int:id>/", unarchive_staff, name="unarchive_staff"),
    path("staff/delete/<int:id>/", delete_staff, name="delete_staff"),
    path("staffs/archived/", archived_staff_list, name="archived_staff_list"),
    # canteen Items
    path("canteen/items/", canteen_item_list, name="canteen_item_list"),
    path("canteen/items/create/", canteen_item_create, name="canteen_item_create"),
    path("items/edit/<int:item_id>/", canteen_item_edit, name="canteen_item_edit"),
    path("archived-items/", archived_items_list_view, name="archived_items_list"),
    path(
        "items/archive/<int:item_id>/",
        canteen_item_archive,
        name="canteen_item_archive",
    ),
    path(
        "items/unarchive/<int:item_id>/",
        canteen_item_unarchive,
        name="unarchive_item",
    ),
    path(
        "items/delete/<int:item_id>/",
        canteen_delete_item,
        name="canteen_delete_item",
    ),
    # cart
    path("cart/", CartListView.as_view(), name="cart_list"),
    path("cart/add/", add_to_cart, name="add_to_cart"),
    path("update-cart-item/<int:item_id>/", update_cart_item, name="update_cart_item"),
    path("delete_cart_item/<int:item_id>/", delete_cart_item, name="delete_cart_item"),
    path("clear_cart/", clear_cart_items, name="clear_cart"),
    # Transaction
    path("canteen/qr_scan_recharge/", qr_scan_recharge_view, name="qr_scan_recharge"),
    path("recharge/<uuid>/", recharge_transaction, name="recharge_transaction"),
    path("canteen/qr_scan_payment/", qr_scan_payment_view, name="qr_scan_payment"),
    path("payment/<uuid>/", payment_transaction, name="payment_transaction"),
    path("cancel_transaction/", cancel_transaction, name="cancel_transaction"),
    path("transactions/", TransactionListView.as_view(), name="transaction_list"),
    path(
        "previous-orders/",
        PreviousOrdersListView.as_view(),
        name="previous_orders_list",
    ),
    # Reports
    path(
        "generate_payment_report_all/",
        generate_payment_report_all,
        name="generate_payment_report_all",
    ),
    path(
        "generate_product_sales_day_based_report_all/",
        generate_product_sales_day_based_report_all,
        name="generate_product_sales_day_based_report_all",
    ),
    path(
        "generate_product_sales_month_based_report_all/",
        generate_product_sales_month_based_report_all,
        name="generate_product_sales_month_based_report_all",
    ),
    path(
        "redirect_transaction_report_page/",
        redirect_transaction_report_page,
        name="redirect_transaction_report_page",
    ),
    path(
        "redirect_sales_report_page/",
        redirect_sales_report_page,
        name="redirect_sales_report_page",
    ),
    path(
        "generate_product_sales_report_all/",
        generate_product_sales_report_all,
        name="generate_product_sales_report_all",
    ),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
