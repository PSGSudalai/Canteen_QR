# BASE/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from BASE.models import CanteenItems, ItemImage
from BASE.forms import CanteenItemForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def canteen_item_list(request):
    if request.user.is_admin:
        items = CanteenItems.objects.filter(is_archieved=False)
    else:
        items = CanteenItems.objects.filter(availability=True, is_archieved=False)

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

    paginator = Paginator(items, 12)  # Show 12 items per page
    page = request.GET.get("page")

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "items": page_obj,
        "is_admin": request.user.is_admin,
        "is_staff": request.user.is_staff,
        "page_obj": page_obj,
    }

    return render(request, "canteen_items/item_list.html", context)


@login_required
def archived_items_list_view(request):
    query = request.GET.get("q", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    archived_items = CanteenItems.objects.filter(is_archieved=True)

    if query:
        archived_items = archived_items.filter(identity__icontains=query)
    if start_date:
        archived_items = archived_items.filter(modified_at__date__gte=start_date)
    if end_date:
        archived_items = archived_items.filter(modified_at__date__lte=end_date)

    return render(
        request,
        "archived_items_list.html",
        {
            "items": archived_items,
            "query": query,
            "start_date": start_date,
            "end_date": end_date,
        },
    )


@login_required
def canteen_item_create(request):
    if not request.user.is_admin:
        return redirect("canteen_item_list")

    if request.method == "POST":
        identity = request.POST.get("identity")
        price = request.POST.get("price")
        availability = request.POST.get("availability") == "on"
        category = request.POST.get("category")
        image = request.FILES.get("image")

        if identity and price and category:
            canteen_item = CanteenItems(
                identity=identity,
                price=price,
                availability=availability,
                category=category,
            )
            canteen_item.save()

            if image:
                item_image = ItemImage(image=image)
                item_image.save()
                canteen_item.itemImage = item_image
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
        image = request.FILES.get("image")

        if identity and price and category:
            item.identity = identity
            item.price = price
            item.availability = availability
            item.category = category
            item.save()

            if image:
                if item.itemImage:
                    item.itemImage.image = image
                    item.itemImage.save()
                else:
                    item_image = ItemImage(canteen_item=item, image=image)
                    item_image.save()
                    item.itemImage = item_image
                    item.save()

            return redirect("canteen_item_list")

    context = {
        "item": item,
        "form_data": {
            "identity": item.identity,
            "price": item.price,
            "availability": item.availability,
            "category": item.category,
            "image": item.itemImage.image.url if item.itemImage else None,
        },
    }
    return render(request, "canteen_items/item_form.html", context)


def canteen_item_archive(request, item_id):
    item = get_object_or_404(CanteenItems, pk=item_id)
    item.is_archieved = True
    item.save()
    return redirect("canteen_item_list")
