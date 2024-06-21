# BASE/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from BASE.models import CanteenItems
from BASE.forms import CanteenItemForm
from django.db.models import Q


@login_required
def canteen_item_list(request):
    items = CanteenItems.objects.filter(availability=True)

    # Filtering based on price range
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price and max_price:
        items = items.filter(price__range=(min_price, max_price))
    elif min_price:
        items = items.filter(price__gte=min_price)
    elif max_price:
        items = items.filter(price__lte=max_price)

    # Filtering based on category (assuming category is a ForeignKey)
    category = request.GET.get("category")
    if category:
        items = items.filter(category=category)

    # Search functionality
    query = request.GET.get("q")
    if query:
        items = items.filter(
            Q(identity__icontains=query) | Q(price__icontains=query)
        ).distinct()

    # Pass user roles to the template
    context = {
        "items": items,
        "is_admin": request.user.is_admin,
        "is_staff": request.user.is_staff,
    }

    return render(request, "canteen_items/item_list.html", context)


def canteen_item_create(request):
    if request.method == "POST":
        form = CanteenItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("canteen_item_list")
    else:
        form = CanteenItemForm()
    return render(request, "canteen_items/item_form.html", {"form": form})
