from django.contrib import admin
from .models import CustomUser, CanteenItems, Transaction, Cart, PreviousOrders


admin.site.register(CustomUser)
admin.site.register(CanteenItems)
admin.site.register(Transaction)
admin.site.register(Cart)
admin.site.register(PreviousOrders)
