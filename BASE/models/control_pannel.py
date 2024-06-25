from django.db import models
from BASE.models import BaseModels
from BASE.choices import CATEGORY_CHOICES, PAYMENT_METHOD, PAYMENT_TYPE


class CanteenItems(BaseModels):
    identity = models.CharField(max_length=100)
    price = models.IntegerField()
    availability = models.BooleanField(default=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="Snacks"
    )
    itemImage = models.ForeignKey(
        "ItemImage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="canteen_items",
    )

    def __str__(self):
        return self.identity


class ItemImage(BaseModels):
    image = models.ImageField(upload_to="canteen_items/")


class Transaction(BaseModels):
    student = models.ForeignKey(
        "BASE.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_student",
    )
    amount = models.IntegerField()
    staff = models.ForeignKey(
        "BASE.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_staff",
    )
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_TYPE, default="Recharge"
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD, default="cash"
    )

    def __str__(self) -> str:
        return f"{self.student} - {self.payment_type}"


class Cart(BaseModels):
    item = models.ForeignKey(CanteenItems, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    is_sold = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.item} - {self.quantity}"
