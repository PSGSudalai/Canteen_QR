from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from BASE.models import CustomUser
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator


@login_required
def staff_list(request):
    query = request.GET.get("q", "")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    page_number = request.GET.get("page", 1)

    if request.user.is_admin:
        users = CustomUser.objects.filter(is_staff=True, is_archieved=False).filter(
            Q(email__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(phone_number__icontains=query)
        )
        if start_date:
            users = users.filter(created_at__date__gte=parse_date(start_date))
        if end_date:
            users = users.filter(created_at__date__lte=parse_date(end_date))
    else:
        users = CustomUser.objects.none()

    paginator = Paginator(users, 12) 
    paginated_users = paginator.get_page(page_number)

    return render(
        request,
        "website/staff_list.html",
        {
            "users": paginated_users,
            "query": query,
            "start_date": start_date,
            "end_date": end_date,
        },
    )


@login_required
def student_list(request):
    query = request.GET.get("q", "")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    page_number = request.GET.get("page", 1)

    if request.user.is_admin:
        users = CustomUser.objects.filter(is_staff=False, is_archieved=False).filter(
            Q(email__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(phone_number__icontains=query)
        )
        if start_date:
            users = users.filter(created_at__date__gte=parse_date(start_date))
        if end_date:
            users = users.filter(created_at__date__lte=parse_date(end_date))
    else:
        users = CustomUser.objects.none()

    paginator = Paginator(users, 12)
    paginated_users = paginator.get_page(page_number)

    return render(
        request,
        "website/student_list.html",
        {
            "users": paginated_users,
            "query": query,
            "start_date": start_date,
            "end_date": end_date,
        },
    )



@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.email = request.POST.get("email", user.email)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.phone_number = request.POST.get("phone_number", user.phone_number)
        user.balance = request.POST.get("balance", user.balance)


        if request.user == user:
            user.is_admin=True
            user.is_staff=True
        else:
            user.is_staff = request.POST.get("is_staff") == "on"
            user.is_admin = request.POST.get("is_admin") == "on"

        user.save()
        return redirect("staff_list" if user.is_staff else "student_list")

    return render(request, "website/edit_user.html", {"user": user})
