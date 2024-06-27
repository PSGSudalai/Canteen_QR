import openpyxl
from openpyxl.utils import get_column_letter
from django.shortcuts import render, redirect
from BASE.models import Transaction, PreviousOrders
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from BASE.choices import PAYMENT_TYPE


@login_required
def generate_payment_report_all(request):
    transactions = Transaction.objects.all()
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    payment_type = request.GET.get("payment_type")

    if start_date:
        transactions = transactions.filter(created_at__date__gte=parse_date(start_date))
    if end_date:
        transactions = transactions.filter(created_at__date__lte=parse_date(end_date))
    if payment_type:
        transactions = transactions.filter(payment_type=payment_type)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Transactions"

    columns = [
        "Student",
        "Amount(₹)",
        "Staff",
        "Payment Type",
        "Payment Method",
        "Date",
        "Time",
    ]
    for col_num, column_title in enumerate(columns, 1):
        column_letter = get_column_letter(col_num)
        ws[f"{column_letter}1"] = column_title

    # Populate the data
    for row_num, transaction in enumerate(transactions, 2):
        ws[
            f"A{row_num}"
        ] = f"{transaction.student.first_name} {transaction.student.last_name}".capitalize()
        ws[f"B{row_num}"] = f"₹ {transaction.amount}"
        ws[
            f"C{row_num}"
        ] = f"{transaction.staff.first_name} {transaction.staff.last_name}".capitalize()
        ws[f"D{row_num}"] = transaction.payment_type
        ws[f"E{row_num}"] = transaction.payment_method
        ws[f"F{row_num}"] = transaction.created_at.strftime("%Y-%m-%d")
        ws[f"G{row_num}"] = transaction.created_at.strftime("%H:%M")

    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[column].width = adjusted_width

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f"attachment; filename=transactions_report_{payment_type}.xlsx"
        if payment_type
        else "attachment; filename=transactions_report.xlsx"
    )
    wb.save(response)
    return response


def redirect_report_page(request):
    return render(request, "generate_report.html")


@login_required
def generate_product_sale_report_all(request):
    orders = PreviousOrders.objects.all()
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date:
        orders = orders.filter(created_at__date__gte=parse_date(start_date))
    if end_date:
        orders = orders.filter(created_at__date__lte=parse_date(end_date))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sales Report"

    columns = [
        "Item",
        "Price (₹)",
        "Monday's Sales Q",
        "Monday's Sales P",
        "Tuesday's Sales Q",
        "Tuesday's Sales P",
        "Wednesday's Sales Q",
        "Wednesday's Sales P",
        "Thursday's Sales Q",
        "Thursday's Sales P",
        "Friday's Sales Q",
        "Friday's Sales P",
        "Saturday's Sales Q",
        "Saturday's Sales P",
        "Sunday's Sales Q",
        "Sunday's Sales P",
    ]
    for col_num, column_title in enumerate(columns, 1):
        column_letter = get_column_letter(col_num)
        ws[f"{column_letter}1"] = column_title

    sales_data = {}

    for order in orders:
        item_name = order.item.identity.capitalize()
        if item_name not in sales_data:
            sales_data[item_name] = {
                "price": order.item.price,
                "monday": {"quantity": 0, "total": 0},
                "tuesday": {"quantity": 0, "total": 0},
                "wednesday": {"quantity": 0, "total": 0},
                "thursday": {"quantity": 0, "total": 0},
                "friday": {"quantity": 0, "total": 0},
                "saturday": {"quantity": 0, "total": 0},
                "sunday": {"quantity": 0, "total": 0},
            }

        day_of_week = order.created_at.strftime("%A").lower()
        sales_data[item_name][day_of_week]["quantity"] += order.quantity
        sales_data[item_name][day_of_week]["total"] += order.total

    for row_num, (item_name, sales) in enumerate(sales_data.items(), 2):
        ws[f"A{row_num}"] = item_name
        ws[f"B{row_num}"] = f"₹ {sales['price']}"

        ws[f"C{row_num}"] = sales["monday"]["quantity"]
        ws[f"D{row_num}"] = f"₹ {sales['monday']['total']}"
        ws[f"E{row_num}"] = sales["tuesday"]["quantity"]
        ws[f"F{row_num}"] = f"₹ {sales['tuesday']['total']}"
        ws[f"G{row_num}"] = sales["wednesday"]["quantity"]
        ws[f"H{row_num}"] = f"₹ {sales['wednesday']['total']}"
        ws[f"I{row_num}"] = sales["thursday"]["quantity"]
        ws[f"J{row_num}"] = f"₹ {sales['thursday']['total']}"
        ws[f"K{row_num}"] = sales["friday"]["quantity"]
        ws[f"L{row_num}"] = f"₹ {sales['friday']['total']}"
        ws[f"M{row_num}"] = sales["saturday"]["quantity"]
        ws[f"N{row_num}"] = f"₹ {sales['saturday']['total']}"
        ws[f"O{row_num}"] = sales["sunday"]["quantity"]
        ws[f"P{row_num}"] = f"₹ {sales['sunday']['total']}"

    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[column].width = adjusted_width

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=sales_report.xlsx"
    wb.save(response)
    return response


def redirect_transaction_report_page(request):
    return render(request, "reports/generate_transaction_report.html")


def redirect_sales_report_page(request):
    return render(request, "reports/generate_sales_report.html")
