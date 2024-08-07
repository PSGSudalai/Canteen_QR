from datetime import datetime
from django.urls import reverse
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponseServerError,
)
from BASE.choices import PAYMENT_TYPE, PAYMENT_METHOD
from BASE.models import Transaction, CustomUser, Cart, PreviousOrders
from BASE.helpers import calculating_total_cost
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q, Sum
from django.utils.dateparse import parse_date
from BASE.helpers import send_email


@method_decorator(login_required, name="dispatch")
class TransactionListView(ListView):
    model = Transaction
    template_name = "website/transaction_list.html"
    paginate_by = 12

    def get_queryset(self):
        try:
            queryset = Transaction.objects.all()
            if self.request.user.is_staff and not self.request.user.is_admin:
                today = datetime.now().date()
                queryset = queryset.filter(created_at__date=today)
            elif not self.request.user.is_admin:
                queryset = queryset.filter(user=self.request.user)

            min_amount = self.request.GET.get("min_amount")
            max_amount = self.request.GET.get("max_amount")
            user_email = self.request.GET.get("user_email")
            start_date = self.request.GET.get("start_date")
            end_date = self.request.GET.get("end_date")
            payment_type = self.request.GET.get("payment_type")
            payment_method = self.request.GET.get("payment_method")

            if min_amount:
                queryset = queryset.filter(amount__gte=min_amount)
            if max_amount:
                queryset = queryset.filter(amount__lte=max_amount)
            if user_email and (
                self.request.user.is_admin or self.request.user.is_staff
            ):
                queryset = queryset.filter(user__email__icontains=(user_email))
            if start_date:
                queryset = queryset.filter(created_at__date__gte=parse_date(start_date))
            if end_date:
                queryset = queryset.filter(created_at__date__lte=parse_date(end_date))
            if payment_type:
                queryset = queryset.filter(payment_type=payment_type)
            if payment_method:
                queryset = queryset.filter(payment_method=payment_method)

            self.total_payments = (
                queryset.filter(payment_type="Payment").aggregate(Sum("amount"))[
                    "amount__sum"
                ]
                or 0
            )
            self.total_recharges = (
                queryset.filter(payment_type="Recharge").aggregate(Sum("amount"))[
                    "amount__sum"
                ]
                or 0
            )

            queryset = queryset.order_by("-created_at")
            return queryset
        except Exception as e:
            raise HttpResponseServerError(
                f"An error occurred while retrieving transactions: {e}"
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add totals to context from the instance variables
        context["total_payments"] = self.total_payments
        context["total_recharges"] = self.total_recharges

        context["user"] = self.request.user
        context["min_amount"] = self.request.GET.get("min_amount", "")
        context["max_amount"] = self.request.GET.get("max_amount", "")
        context["user_email"] = self.request.GET.get("user_email", "")
        context["start_date"] = self.request.GET.get("start_date", "")
        context["end_date"] = self.request.GET.get("end_date", "")
        context["payment_type"] = self.request.GET.get("payment_type", "")
        context["payment_method"] = self.request.GET.get("payment_method", "")
        context["payment_types"] = PAYMENT_TYPE
        context["payment_methods"] = PAYMENT_METHOD
        return context


@login_required
def recharge_transaction(request, uuid):
    if request.method == "POST":
        amount = request.POST.get("amount")
        payment_method = request.POST.get("payment_method", "cash")
        staff = request.user

        if not staff.is_staff:
            return HttpResponseBadRequest("Permission denied")

        try:
            user = CustomUser.objects.get(uuid=uuid, is_archieved=False)
        except CustomUser.DoesNotExist:
            return HttpResponseBadRequest("User not found")

        try:
            amount = int(amount)
            if amount <= 0:
                return HttpResponseBadRequest("Invalid amount")
            user.balance += amount
            user.save()
        except ValueError:
            return HttpResponseBadRequest("Invalid amount")

        try:
            Transaction.objects.create(
                user=user,
                amount=amount,
                staff=staff,
                payment_type="Recharge",
                payment_method=payment_method,
            )
        except Exception as e:
            return HttpResponseServerError(
                f"An error occurred while creating the transaction: {e}"
            )

        next_url = (
            request.POST.get("next")
            or request.GET.get("next")
            or reverse("canteen_item_list")
        )
        return HttpResponseRedirect(next_url)

    elif request.method == "GET":
        try:
            user = CustomUser.objects.get(uuid=uuid, is_archieved=False)
        except CustomUser.DoesNotExist:
            return HttpResponseBadRequest("User not found")

        context = {
            "uuid": uuid,
            "user": user,
            "next": request.GET.get("next", ""),
        }
        return render(request, "website/recharge_form.html", context)
    else:
        return HttpResponseBadRequest("Method not allowed")


@login_required
def payment_transaction(request, uuid):
    try:
        user = CustomUser.objects.get(uuid=uuid, is_archieved=False)
    except CustomUser.DoesNotExist:
        return HttpResponseBadRequest("User not found")

    try:
        cartItems = Cart.objects.filter(is_sold=False)
        total_amount = calculating_total_cost(cartItems)
    except Exception as e:
        return HttpResponseServerError(
            f"An error occurred while calculating the total cost: {e}"
        )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "recharge":
            next_url = reverse("payment_transaction", kwargs={"uuid": user.uuid})
            return redirect(
                f"{reverse('recharge_transaction', kwargs={'uuid': user.uuid})}?next={next_url}"
            )

        if action == "cancel":
            return redirect("cart_list")

        payment_method = request.POST.get("payment_method", "cash")
        staff = request.user

        if not staff.is_staff:
            return HttpResponseBadRequest("Permission denied")

        try:
            amount = int(total_amount)
            if user.balance < amount:
                return render(
                    request,
                    "website/insufficient_balance.html",
                    {"user": user, "total_amount": total_amount},
                )
            user.balance -= amount
            user.save()
        except ValueError:
            return HttpResponseBadRequest("Invalid amount")
        except Exception as e:
            return HttpResponseServerError(
                f"An error occurred while updating the user's balance: {e}"
            )

        try:
            transaction = Transaction.objects.create(
                user=user,
                amount=amount,
                staff=staff,
                payment_type="Payment",
                payment_method=payment_method,
            )

            for cartItem in cartItems:
                PreviousOrders.objects.create(
                    user=user,
                    staff=staff,
                    item=cartItem.item,
                    item_name=cartItem.item.identity,
                    item_price=cartItem.item.price,
                    quantity=cartItem.quantity,
                    total=cartItem.quantity * cartItem.item.price,
                )

            cartItems.update(is_sold=True)
            cartItems.delete()
        except Exception as e:
            return HttpResponseServerError(
                f"An error occurred while processing the transaction: {e}"
            )

        return redirect("canteen_item_list")

    elif request.method == "GET":
        return render(
            request,
            "website/payment_form.html",
            {"user": user, "total_amount": total_amount},
        )
    else:
        return HttpResponseBadRequest("Method not allowed")


def cancel_transaction(request):
    try:
        Cart.objects.all().delete()
    except Exception as e:
        return HttpResponseServerError(
            f"An error occurred while canceling the transaction: {e}"
        )
    return redirect("canteen_item_list")
