from django.views.generic import ListView
from BASE.models import PreviousOrders
from django.contrib.auth.mixins import LoginRequiredMixin


class PreviousOrdersListView(ListView):
    model = PreviousOrders
    template_name = "website/previous_orders_list.html"

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_staff:
            return PreviousOrders.objects.all()
        else:
            return PreviousOrders.objects.filter(student=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
