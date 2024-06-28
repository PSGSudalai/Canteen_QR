from django.views.generic import ListView
from BASE.models import PreviousOrders
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils.dateparse import parse_date


class PreviousOrdersListView(LoginRequiredMixin, ListView):
    model = PreviousOrders
    template_name = "website/previous_orders_list.html"
    paginate_by = 15

    def get_queryset(self):
        queryset = (
            PreviousOrders.objects.all().order_by('-created_at')
            if self.request.user.is_admin or self.request.user.is_staff
            else PreviousOrders.objects.filter(student=self.request.user).order_by('-created_at')
        )

        min_total = self.request.GET.get("min_total")
        max_total = self.request.GET.get("max_total")
        user_email = self.request.GET.get("user_email")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        if min_total:
            queryset = queryset.filter(total__gte=min_total)
        if max_total:
            queryset = queryset.filter(total__lte=max_total)
        if user_email and (self.request.user.is_admin or self.request.user.is_staff):
            queryset = queryset.filter(student__email__icontains=user_email)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(created_at__date__lte=parse_date(end_date))

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["min_total"] = self.request.GET.get("min_total", "")
        context["max_total"] = self.request.GET.get("max_total", "")
        context["user_email"] = self.request.GET.get("user_email", "")
        context["start_date"] = self.request.GET.get("start_date", "")
        context["end_date"] = self.request.GET.get("end_date", "")
        return context
