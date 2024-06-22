from django.views.generic import ListView
from BASE.models import PreviousOrders
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class PreviousOrdersListView(LoginRequiredMixin, ListView):
    model = PreviousOrders
    template_name = "website/previous_orders_list.html"

    def get_queryset(self):
        queryset = (
            PreviousOrders.objects.all()
            if self.request.user.is_admin or self.request.user.is_staff
            else PreviousOrders.objects.filter(student=self.request.user)
        )

        min_amount = self.request.GET.get("min_amount")
        max_amount = self.request.GET.get("max_amount")
        user_email = self.request.GET.get("user_email")

        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)
        if user_email and (self.request.user.is_admin or self.request.user.is_staff):
            queryset = queryset.filter(student__email__icontains=user_email)

        return queryset

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["min_total"] = self.request.GET.get("min_total", "")
        context["max_total"] = self.request.GET.get("max_total", "")
        context["user_email"] = self.request.GET.get("user_email", "")
        return context
