# BASE/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from BASE.models import CustomUser
import uuid
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO


def signup_view(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(
                request, "Email address is already in use. Please use another email."
            )

        else:
            # Create the user
            user = CustomUser.objects.create_user(
                email=email,
                password=password1,
                first_name=firstname,
                last_name=lastname,
            )

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(user.uuid)
            qr.make(fit=True)

            # Generate QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Save QR code image to user model
            qr_img_buffer = BytesIO()
            qr_img.save(qr_img_buffer, format="PNG")
            filename = f"qr_code_{user.id}.png"  # Unique filename for each user
            user.qr_code.save(filename, ContentFile(qr_img_buffer.getvalue()))
            user.save()

            # Login user
            login(request, user)
            # messages.success(request, "Registration successful")
            return redirect(
                "qr_image"
            )  # Redirect to a view that displays/shares the QR image

    return render(request, "registration/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("canteen_item_list")
        else:
            messages.error(request, "Invalid UserName or Password")
            return redirect("login")

    return render(request, "registration/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def qr_image_view(request):
    user = request.user

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(user.uuid)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_img_buffer = BytesIO()
    qr_img.save(qr_img_buffer, format="PNG")
    filename = f"qr_code_{user.id}.png"
    user.qr_code.save(filename, ContentFile(qr_img_buffer.getvalue()))
    user.save()

    return render(request, "qr_image.html", {"user": user})
