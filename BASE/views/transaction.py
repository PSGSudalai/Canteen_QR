# BASE/views/transaction.py
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from BASE.models import Transaction, CustomUser, Cart, PreviousOrders
from BASE.helpers import calculating_total_cost
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q


@method_decorator(login_required, name="dispatch")
class TransactionListView(ListView):
    model = Transaction
    template_name = "website/transaction_list.html"

    def get_queryset(self):
        queryset = (
            Transaction.objects.all()
            if self.request.user.is_admin or self.request.user.is_staff
            else Transaction.objects.filter(student=self.request.user)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["min_amount"] = self.request.GET.get("min_amount", "")
        context["max_amount"] = self.request.GET.get("max_amount", "")
        context["user_email"] = self.request.GET.get("user_email", "")
        return context


def recharge_transaction(request, uuid):
    if request.method == "POST":
        amount = request.POST.get("amount")
        payment_method = request.POST.get("payment_method", "cash")
        staff = request.user

        if not staff.is_staff:
            return HttpResponseBadRequest("Permission denied")

        try:
            student = CustomUser.objects.get(uuid=uuid)
        except CustomUser.DoesNotExist:
            return HttpResponseBadRequest("Student not found")

        try:
            amount = int(amount)
            student.balance += amount
            student.save()

        except ValueError:
            return HttpResponseBadRequest("Invalid amount")

        transaction = Transaction.objects.create(
            student=student,
            amount=amount,
            staff=staff,
            payment_type="Recharge",
            payment_method=payment_method,
        )
        # Optionally send email notification
        # send_email("Recharge", amount, student.email)

        return redirect(
            "canteen_item_list"
        )  # Redirect to transaction list or any other appropriate page

    elif request.method == "GET":
        # Fetch the student object
        try:
            student = CustomUser.objects.get(uuid=uuid)
        except CustomUser.DoesNotExist:
            return HttpResponseBadRequest("Student not found")

        # Render the form with student's first name and last name separately
        context = {
            "uuid": uuid,
            "student": student,  # Pass the student object itself to access first_name and last_name in the template
        }
        return render(request, "website/recharge_form.html", context)


@login_required
def payment_transaction(request, uuid):
    try:
        student = CustomUser.objects.get(uuid=uuid)
    except CustomUser.DoesNotExist:
        return HttpResponseBadRequest("Student not found")

    cartItems = Cart.objects.filter(is_sold=False)
    total_amount = calculating_total_cost(cartItems)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "recharge":
            return redirect("recharge_page_url")  # Replace with your recharge page URL

        if action == "cancel":
            return redirect("cart_page_url")  # Replace with your cart page URL

        payment_method = request.POST.get("payment_method", "cash")
        staff = request.user

        if not staff.is_staff:
            return HttpResponseBadRequest("Permission denied")

        try:
            amount = int(total_amount)
            if student.balance < amount:
                return render(
                    request,
                    "website/insufficient_balance.html",
                    {"student": student, "total_amount": total_amount},
                )
            student.balance -= amount
            student.save()
        except ValueError:
            return HttpResponseBadRequest("Invalid amount")

        # Record the transaction
        transaction = Transaction.objects.create(
            student=student,
            amount=amount,
            staff=staff,
            payment_type="Payment",
            payment_method=payment_method,
        )

        # Store previous orders
        for cartItem in cartItems:
            PreviousOrders.objects.create(
                student=student,
                staff=staff,
                item=cartItem.item,
                quantity=cartItem.quantity,
                total=cartItem.quantity * cartItem.item.price,
            )

        cartItems.update(is_sold=True)
        # send_email("Payment", amount, student.email)
        return redirect(
            "canteen_item_list"
        )  # Redirect to transaction list or any other appropriate page

    elif request.method == "GET":
        return render(
            request,
            "website/payment_form.html",
            {"student": student, "total_amount": total_amount},
        )

    else:
        return HttpResponseBadRequest("Method not allowed")
