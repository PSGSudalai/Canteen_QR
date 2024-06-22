from django.shortcuts import get_object_or_404, redirect, render
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


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.email = request.POST.get("email", user.email)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.phone_number = request.POST.get("phone_number", user.phone_number)
        user.balance = request.POST.get("balance", user.balance)
        user.save()
        return redirect("staff_list" if user.is_staff else "student_list")

    return render(request, "website/edit_user.html", {"user": user})
