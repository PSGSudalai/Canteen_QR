from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from BASE.models import CustomUser
from BASE.helpers import send_welcome_email
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO


def signup_view(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password1 = request.POST.get("password1")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(
                request, "Email address is already in use. Please use another email.", extra_tags='signup'
            )
        else:
            # Create the user
            user = CustomUser.objects.create_user(
                email=email,
                phone_number=phone_number,
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

            qr_img_buffer = BytesIO()
            qr_img.save(qr_img_buffer, format="PNG")
            filename = f"qr_code_{user.id}.png"
            user.qr_code.save(filename, ContentFile(qr_img_buffer.getvalue()))
            user.save()

            attachment = {
                "filename": filename,
                "content": qr_img_buffer.getvalue(),
                "mimetype": "image/png",
            }

            # send_welcome_email(
            #     subject="Welcome to Our Service",
            #     message="Thank you for signing up. Please find your QR code attached.",
            #     email=user.email,
            #     attachment=attachment,
            # )

            return redirect("qr_image", user_id=user.id)

    return render(request, "registration/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=(password or 0000))
        if user is not None:
            login(request, user)
            return redirect("canteen_item_list")
        else:
            messages.error(request, "Invalid UserName or Password", extra_tags='login')
            return redirect("login")

    return render(request, "registration/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def qr_image_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

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


@login_required
def balance_check_view(request):
    user_balance = request.user.balance

    return render(
        request,
        "website/balance_check_template.html",
        {"user": request.user, "user_balance": user_balance},
    )


@login_required
def archive_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.is_archieved = True
    user.save()
    return redirect("student_list")


@login_required
def unarchive_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.is_archieved = False
    user.save()
    return redirect("archived_student_list")


@login_required
def archived_student_list(request):
    users = CustomUser.objects.filter(is_archieved=True)
    return render(request, "website/archived_student_list.html", {"users": users})
