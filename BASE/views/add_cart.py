# BASE/views/add_cart.py
from django.shortcuts import render, redirect, get_object_or_404
from BASE.models import CanteenItems, Cart
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from BASE.helpers import calculating_total_cost
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError


def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        quantity = request.POST.get("quantity", 1)

        if not item_id:
            return JsonResponse({"error": "Item ID is required"}, status=400)

        try:
            item = get_object_or_404(CanteenItems, id=item_id)
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError("Quantity must be at least 1")
        except (ValueError, ObjectDoesNotExist) as e:
            return JsonResponse({"error": str(e)}, status=400)

        try:
            cart_item, created = Cart.objects.get_or_create(
                item=item, defaults={"quantity": quantity}, is_sold=False
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

        return redirect("canteen_item_list")

    return JsonResponse({"error": "Invalid request method"}, status=400)


def update_cart_item(request, item_id):
    if request.method == "POST":
        quantity = request.POST.get("quantity")

        if not quantity:
            return HttpResponseBadRequest("Quantity is required")

        try:
            cart_item = Cart.objects.get(id=item_id)
            cart_item.quantity = int(quantity)
            if cart_item.quantity < 1:
                raise ValueError("Quantity must be at least 1")
            cart_item.is_sold = False
            cart_item.save()
        except Cart.DoesNotExist:
            return HttpResponseBadRequest("Cart item not found")
        except ValueError as e:
            return HttpResponseBadRequest(str(e))
        except ValidationError as e:
            return HttpResponseBadRequest(str(e))

        return redirect("cart_list")
    return HttpResponseBadRequest("Method not allowed")


@require_POST
def clear_cart_items(request):
    try:
        Cart.objects.filter(is_sold=False).delete()
    except Exception as e:
        return HttpResponseBadRequest(f"Failed to clear cart items: {str(e)}")
    return redirect("cart_list")


@require_POST
def delete_cart_item(request, item_id):
    try:
        item = get_object_or_404(Cart, id=item_id, is_sold=False)
        item.delete()
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Cart item not found")
    except Exception as e:
        return HttpResponseBadRequest(f"Failed to delete cart item: {str(e)}")
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
