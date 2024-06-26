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
        ws[f"A{row_num}"] = f"{transaction.student.first_name} {transaction.student.last_name}".capitalize()
        ws[f"B{row_num}"] = f"₹ {transaction.amount}"
        ws[f"C{row_num}"] = f"{transaction.staff.first_name} {transaction.staff.last_name}".capitalize()
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
    response["Content-Disposition"] = f"attachment; filename=transactions_report_{payment_type}.xlsx" if payment_type else "attachment; filename=transactions_report.xlsx"
    wb.save(response)
    return response

def redirect_report_page(request):
    return render(request, "generate_report.html")



@login_required
def generate_product_sale_report_all(request):
    orders=PreviousOrders.objects.all()
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
        "Price(₹)",
        "Quantity",
        "Total",
        "Date",
        "Time",
        "Day",
    ]
    for col_num, column_title in enumerate(columns, 1):
        column_letter = get_column_letter(col_num)
        ws[f"{column_letter}1"] = column_title

    for row_num, item in enumerate(orders, 2):
        ws[f"A{row_num}"] = f"{item.item.identity}".capitalize()
        ws[f"B{row_num}"] = f"₹ {item.item.price}"
        ws[f"C{row_num}"] =item.quantity
        ws[f"D{row_num}"] = item.toatal
        ws[f"E{row_num}"] = item.created_at.strftime("%Y-%m-%d")
        ws[f"F{row_num}"] = item.created_at.strftime("%H:%M")
        ws[f"F{row_num}"] = item.created_at.strftime("%D")

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