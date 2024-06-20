# BASE/views.py

from django.shortcuts import render, redirect
from BASE.models import CanteenItems
from BASE.forms import CanteenItemForm


def canteen_item_list(request):
    items = CanteenItems.objects.all()
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
