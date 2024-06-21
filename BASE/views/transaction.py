# BASE/views/transaction.py
from django.views.generic import ListView
from BASE.models import Transaction


class TransactionListView(ListView):
    model = Transaction
    template_name = "website/transaction_list.html"

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_staff:
            return Transaction.objects.all()
        else:
            return Transaction.objects.filter(student=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
