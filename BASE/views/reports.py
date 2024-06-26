import openpyxl
from openpyxl.utils import get_column_letter
from django.shortcuts import render, redirect
from BASE.models import Transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.dateparse import parse_date

@login_required
def generate_report_all(request):
    transactions = Transaction.objects.all()
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date:
        transactions = transactions.filter(created_at__date__gte=parse_date(start_date))
    if end_date:
        transactions = transactions.filter(created_at__date__lte=parse_date(end_date))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Transactions"

    columns = [
        "Student",
        "Amount",
        "Staff",
        "Payment Type",
        "Payment Method",
        "Date",
    ]
    for col_num, column_title in enumerate(columns, 1):
        column_letter = get_column_letter(col_num)
        ws[column_letter + "1"] = column_title

    # Populate the data
    for row_num, transaction in enumerate(transactions, 2):
        ws[f"A{row_num}"] = str(transaction.student)
        ws[f"B{row_num}"] = transaction.amount
        ws[f"C{row_num}"] = str(transaction.staff)
        ws[f"D{row_num}"] = transaction.payment_type
        ws[f"E{row_num}"] = transaction.payment_method
        ws[f"F{row_num}"] = transaction.created_at.strftime("%Y-%m-%d %H:%M")

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
    response["Content-Disposition"] = "attachment; filename=transactions_report.xlsx"
    wb.save(response)
    return response


def redirect_report_page(request):
    return render(request, "generate_report.html")