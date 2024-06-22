# BASE/views/transaction.py
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from BASE.models import Transaction, CustomUser, Cart, PreviousOrders
from BASE.helpers import calculating_total_cost


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
            "transaction_list"
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


def payment_transaction(request, uuid):
    if request.method == "POST":
        payment_method = request.POST.get("payment_method", "cash")
        staff = request.user

        if not staff.is_staff:
            return HttpResponseBadRequest("Permission denied")

        try:
            student = CustomUser.objects.get(uuid=uuid)
        except CustomUser.DoesNotExist:
            return HttpResponseBadRequest("Student not found")

        cartItems = Cart.objects.filter(is_sold=False)
        amount = calculating_total_cost(cartItems)

        try:
            amount = int(amount)
            if student.balance < amount:
                return HttpResponseBadRequest("Insufficient balance")
            student.balance -= amount
            student.save()
        except ValueError:
            return HttpResponseBadRequest("Invalid amount")

        transaction = Transaction.objects.create(
            student=student,
            amount=amount,
            staff=staff,
            payment_type="Payment",
            payment_method=payment_method,
        )

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
            "transaction_list"
        )  # Redirect to transaction list or any other appropriate page

    elif request.method == "GET":
        # Render the form for GET requests
        return render(request, "website/payment_form.html", {"uuid": uuid})

    else:
        return HttpResponseBadRequest("Method not allowed")
