from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def qr_scan_recharge_view(request):
    return render(request, "qr_scan_recharge.html")


@login_required
def qr_scan_payment_view(request):
    return render(request, "qr_scan_payment.html")


def custom_404_view(request, exception=None):
    return render(request, "website/404.html", status=404)
