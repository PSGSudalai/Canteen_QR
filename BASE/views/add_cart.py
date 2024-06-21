# BASE/views.py

from django.shortcuts import render, redirect, get_object_or_404
from BASE.models import CanteenItems, Cart
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.decorators.http import require_POST


def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        quantity = int(request.POST.get("quantity", 1))

        item = get_object_or_404(CanteenItems, id=item_id)
        cart_item, created = Cart.objects.get_or_create(
            item=item, defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect("cart_list")  # Redirect to the cart list view

    return JsonResponse({"error": "Invalid request method"}, status=400)


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
