from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from BASE.models import CustomUser


@login_required
def staff_list(request):
    if request.user.is_admin:
        users = CustomUser.objects.filter(is_staff=True)
    else:
        users = CustomUser.objects.none()
    return render(request, "website/staff_list.html", {"users": users})


@login_required
def student_list(request):
    if request.user.is_admin:
        users = CustomUser.objects.filter(is_staff=False)
    else:
        users = CustomUser.objects.none()
    return render(request, "website/student_list.html", {"users": users})
