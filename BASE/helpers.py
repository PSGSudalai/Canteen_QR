import requests
from twilio.rest import Client
from django.conf import settings
from django.shortcuts import render


TEXTLOCAL_API_KEY = "NDczNzU3NDU1MjZiNTY0NDcyNjg1MTUwNzg1MzUwNTQ="
TEXTLOCAL_SENDER = "TXTLCL"


def send_sms(to, message):
    api_key = TEXTLOCAL_API_KEY
    sender = TEXTLOCAL_SENDER
    numbers = to
    message = message

    data = {"apikey": api_key, "numbers": numbers, "message": message, "sender": sender}

    response = requests.post("https://api.textlocal.in/send/", data=data)
    return response.json()


def send_message(type="welcome", amount=0, number=None):
    to_number = "+91" + number if number else "+916382723746"
    if type == "recharge":
        message_body = f"Your recharge of {amount} was successful"
    elif type == "payment":
        message_body = f"Your payment of {amount} was successful"
    else:
        message_body = "Welcome!"

    message = send_sms(to_number, message_body)

    if message:
        print(f"Message sent to {to_number}: {message_body}")
    else:
        print(f"Failed to send message to {to_number}")


def calculating_total_cost(cart_items):
    total_cost = sum(item.item.price * item.quantity for item in cart_items)
    return total_cost if total_cost else 0
