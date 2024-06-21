from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def qr_scan_view(request):
    return render(request, "qr_scan.html")
