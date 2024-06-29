from BASE.models import BaseModels, CanteenItems, CustomUser
from django.db import models


class PreviousOrders(BaseModels):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="user_student_order",
        null=True,
    )
    staff = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_staff_order",
    )
    item = models.ForeignKey(CanteenItems, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.student} - {self.total}"
