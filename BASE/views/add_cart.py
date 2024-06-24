# BASE/views.py
from django.shortcuts import render, redirect, get_object_or_404
from BASE.models import CanteenItems, Cart
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from BASE.helpers import calculating_total_cost
from django.contrib import messages


def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        quantity = int(request.POST.get("quantity", 1))

        item = get_object_or_404(CanteenItems, id=item_id)
        cart_item, created = Cart.objects.get_or_create(
            item=item, defaults={"quantity": quantity}, is_sold=False
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, f"{item.identity} added to cart")

        return redirect("cart_list")  # Redirect to the cart list view

    return JsonResponse({"error": "Invalid request method"}, status=400)


def update_cart_item(request, item_id):
    if request.method == "POST":
        quantity = request.POST.get("quantity")

        try:
            cart_item = Cart.objects.get(id=item_id)
        except Cart.DoesNotExist:
            return HttpResponseBadRequest("Cart item not found")

        try:
            cart_item.quantity = int(quantity)
            cart_item.is_sold = False
            cart_item.save()
        except ValueError:
            return HttpResponseBadRequest("Invalid quantity")

        return redirect("cart_list")
    return HttpResponseBadRequest("Method not allowed")


@require_POST
def clear_cart_items(request):
    Cart.objects.filter(is_sold=False).delete()
    return redirect("cart_list")


@require_POST
def delete_cart_item(request, item_id):
    item = get_object_or_404(Cart, id=item_id, is_sold=False)
    item.delete()
    return redirect("cart_list")


class CartListView(ListView):
    model = Cart
    template_name = "cart/cart_list.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        return Cart.objects.filter(is_sold=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()

        # Calculate total cost for items in the cart
        total_cost = sum(item.item.price * item.quantity for item in cart_items)

        context["total_cost"] = total_cost
        context["cart_items"] = cart_items
        return context
