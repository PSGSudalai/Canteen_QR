from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from BASE.models import CustomUser
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest


@login_required
def staff_list(request):
    try:
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
    except Exception as e:
        return HttpResponseBadRequest(f"Error fetching staff list: {str(e)}")


@login_required
def student_list(request):
    try:
        query = request.GET.get("q", "")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        page_number = request.GET.get("page", 1)

        if request.user.is_admin:
            users = CustomUser.objects.filter(
                is_staff=False, is_archieved=False
            ).filter(
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
    except Exception as e:
        return HttpResponseBadRequest(f"Error fetching student list: {str(e)}")
