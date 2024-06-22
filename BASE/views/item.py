# BASE/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from BASE.models import CanteenItems
from BASE.forms import CanteenItemForm
from django.db.models import Q


@login_required
def canteen_item_list(request):
    if request.user.is_admin:
        items = CanteenItems.objects.all()
    else:
        items = CanteenItems.objects.filter(availability=True)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price and max_price:
        items = items.filter(price__range=(min_price, max_price))
    elif min_price:
        items = items.filter(price__gte=min_price)
    elif max_price:
        items = items.filter(price__lte=max_price)

    category = request.GET.get("category")
    if category:
        items = items.filter(category=category)

    query = request.GET.get("q")
    if query:
        items = items.filter(
            Q(identity__icontains=query) | Q(price__icontains=query)
        ).distinct()

    context = {
        "items": items,
        "is_admin": request.user.is_admin,
        "is_staff": request.user.is_staff,
    }

    return render(request, "canteen_items/item_list.html", context)


@login_required
def canteen_item_create(request):
    if not request.user.is_admin:
        return redirect("canteen_item_list")

    if request.method == "POST":
        identity = request.POST.get("identity")
        price = request.POST.get("price")
        availability = request.POST.get("availability") == "on"
        category = request.POST.get("category")

        if identity and price and category:
            canteen_item = CanteenItems(
                identity=identity,
                price=price,
                availability=availability,
                category=category,
            )
            canteen_item.save()
            return redirect("canteen_item_list")
    return render(request, "canteen_items/item_form.html")


@login_required
def canteen_item_edit(request, item_id):
    if not request.user.is_admin:
        return redirect("canteen_item_list")

    item = get_object_or_404(CanteenItems, id=item_id)

    if request.method == "POST":
        identity = request.POST.get("identity")
        price = request.POST.get("price")
        availability = request.POST.get("availability") == "on"
        category = request.POST.get("category")

        if identity and price and category:
            item.identity = identity
            item.price = price
            item.availability = availability
            item.category = category
            item.save()
            return redirect("canteen_item_list")

    context = {
        "item": item,
        "form_data": {
            "identity": item.identity,
            "price": item.price,
            "availability": item.availability,
            "category": item.category,
        },
    }
    return render(request, "canteen_items/item_form.html", context)


def canteen_item_archive(request, item_id):
    item = get_object_or_404(CanteenItems, pk=item_id)
    item.is_archive = True
    item.save()
    return redirect("canteen_item_list")
