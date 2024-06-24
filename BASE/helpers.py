from Canteen_QR import settings
from django.shortcuts import render
from django.core.mail import send_mail


def send_email(type, amount, email):
    # EMAIL_HOST_USER = "mforspamers@gmail.com"
    message = "This is a test email sent from a Django application."
    recipient_list = [email]
    if type == "recharge":
        subject = f"Your recharge of {amount} was successful"
    elif type == "payment":
        subject = f"Your payment of {amount} was successful"
    else:
        subject = "Welcome!"

    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)


def calculating_total_cost(cart_items):
    total_cost = sum(item.item.price * item.quantity for item in cart_items)
    return total_cost if total_cost else 0


from twilio.rest import Client


def send_sms(to_number, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=body, from_=settings.TWILIO_PHONE_NUMBER, to=to_number
    )

    return message.sid


from django.shortcuts import render
from django.http import HttpResponse
from .helpers import send_sms


def send_sms_view(message):
    to_number = "+918110015692"
    message_body = message if message else "Hello from Twilio!"

    message_sid = send_sms(to_number, message_body)

    return HttpResponse(f"SMS sent with SID: {message_sid}")
