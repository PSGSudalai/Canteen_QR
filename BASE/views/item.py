# BASE/views.py

from django.shortcuts import render, redirect
from BASE.models import CanteenItems
from BASE.forms import CanteenItemForm
from django.db.models import Q


def canteen_item_list(request):
    items = CanteenItems.objects.filter(
        availability=True
    )  # Filter available items only

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
        items = items.filter(category__name=category)

    # Search functionality
    query = request.GET.get("q")
    if query:
        items = items.filter(
            Q(identity__icontains=query)
            | Q(  # Case-insensitive search by identity
                price__icontains=query
            )  # Case-insensitive search by price (if applicable)
        ).distinct()  # Ensure distinct results

    return render(request, "canteen_items/item_list.html", {"items": items})


def canteen_item_create(request):
    if request.method == "POST":
        form = CanteenItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("canteen_item_list")
    else:
        form = CanteenItemForm()
    return render(request, "canteen_items/item_form.html", {"form": form})
