from .user import (
    login_view,
    signup_view,
    logout_view,
    edit_user,
    qr_image_view,
    balance_check_view,
    archive_user,
    archive_staff,
    unarchive_user,
    unarchive_staff,
    archived_student_list,
    archived_staff_list,
    delete_user,
    delete_staff,
)
from .item import (
    canteen_item_create,
    canteen_item_list,
    canteen_item_edit,
    canteen_item_archive,
    archived_items_list_view,
    canteen_item_unarchive,
    canteen_delete_item,
)
from .add_cart import (
    add_to_cart,
    CartListView,
    clear_cart_items,
    delete_cart_item,
    update_cart_item,
)

from .previous_order import PreviousOrdersListView
from .transaction import (
    TransactionListView,
    recharge_transaction,
    payment_transaction,
    cancel_transaction,
)
from .user_list import staff_list, student_list
from .reports import (
    generate_payment_report_all,
    generate_product_sales_day_based_report_all,
    generate_product_sales_month_based_report_all,
    redirect_transaction_report_page,
    generate_product_sales_report_all,
    redirect_sales_report_page,
)
from .redirect import (
    qr_scan_payment_view,
    qr_scan_recharge_view,
    custom_404_view,
)
