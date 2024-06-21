from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from BASE.models import CustomUser, Transaction, Cart, PreviousOrders
from BASE.helpers import calculating_total_cost


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def recharge_transaction_view(request):
    uuid = request.data.get("uuid")
    staff = request.user

    if not staff.is_staff:
        return Response(
            {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )

    student = get_object_or_404(CustomUser, uuid=uuid)
    amount = request.data.get("amount")
    payment_type = "Recharge"
    payment_method = request.data.get("payment_method", "cash")

    try:
        amount = int(amount)
        student.balance += amount
        student.save()
    except ValueError:
        return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

    transaction = Transaction.objects.create(
        student=student,
        amount=amount,
        staff=staff,
        payment_type=payment_type,
        payment_method=payment_method,
    )
    # send_email(payment_type, amount, student.email)
    return Response(
        {
            "message": "Transaction made successfully",
            "transaction_id": transaction.id,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def payment_transaction_view(request):
    uuid = request.data.get("uuid")
    staff = request.user

    if not staff.is_staff:
        return Response(
            {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )

    student = get_object_or_404(CustomUser, uuid=uuid)
    cart_items = Cart.objects.filter(is_sold=False)
    amount = calculating_total_cost(cart_items)
    payment_type = "Payment"
    payment_method = request.data.get("payment_method", "cash")

    try:
        amount = int(amount)
        if student.balance < amount:
            return Response(
                {"error": "Insufficient balance"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        student.balance -= amount
        student.save()
    except ValueError:
        return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

    transaction = Transaction.objects.create(
        student=student,
        amount=amount,
        staff=staff,
        payment_type=payment_type,
        payment_method=payment_method,
    )

    for cart_item in cart_items:
        PreviousOrders.objects.create(
            student=student,
            staff=staff,
            item=cart_item.item,
            quantity=cart_item.quantity,
            total=cart_item.quantity * cart_item.item.price,
        )

    cart_items.update(is_sold=True)
    # send_email(payment_type, amount, student.email)
    return Response(
        {
            "message": "Transaction made successfully",
            "transaction_id": transaction.id,
        },
        status=status.HTTP_201_CREATED,
    )
