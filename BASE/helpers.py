from Canteen_QR import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.mail import EmailMessage


def send_welcome_email(subject, message, email, attachment=None):
    recipient_list = [email]
    email_message = EmailMessage(
        subject, message, settings.EMAIL_HOST_USER, recipient_list
    )
    if attachment:
        email_message.attach(
            attachment["filename"], attachment["content"], attachment["mimetype"]
        )
    email_message.send()


def send_email(type, amount, email):
    # EMAIL_HOST_USER = "mforspamers@gmail.com"
    recipient_list = [email]
    if type == "recharge":
        subject = "Recharge Successful Email"
        message = f"Your recharge of {amount} was successful"
    elif type == "payment":
        subject = "Payment Successful Email"
        message = f"Your payment of {amount} was successful"

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



def send_sms_view(message="hello"):
    to_number = "+918110015692"
    message_body = message if message else "Hello from Twilio!"

    message_sid = send_sms(to_number, message_body)

    return HttpResponse(f"SMS sent with SID: {message_sid}")
