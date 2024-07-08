from django.http import HttpResponseBadRequest
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
        is_user = request.POST.get("is_user") == "on"
        is_staff = request.POST.get("is_staff") == "on"
        is_admin = request.POST.get("is_admin") == "on"

        if CustomUser.objects.filter(email=email).exists():
            messages.error(
                request,
                "Email address is already in use. Please use another email.",
                extra_tags="signup",
            )
        else:
            # Create the user
            user = CustomUser.objects.create_user(
                email=email,
                phone_number=phone_number,
                password=password1,
                first_name=firstname,
                last_name=lastname,
                is_user=True,
                is_staff=is_staff,
                is_admin=is_admin,
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

            send_welcome_email(
                subject="Welcome to Our Service",
                message="Thank you for signing up. Please find your QR code attached.",
                email=user.email,
                attachment=attachment,
            )

            return redirect("qr_image", uuid=user.uuid)

    return render(request, "registration/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(
                request, "Please enter both email and password.", extra_tags="login"
            )
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("canteen_item_list")
        else:
            messages.error(request, "Invalid email or password.", extra_tags="login")
            return redirect("login")

    return render(request, "registration/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def qr_image_view(request, uuid):
    user = get_object_or_404(CustomUser, uuid=uuid)

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
def archive_staff(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.is_archieved = True
    user.save()
    return redirect("staff_list")


@login_required
def delete_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if user.is_archieved:
        user.delete()
    return redirect("student_list")


@login_required
def delete_staff(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if user.is_archieved:
        user.delete()
    return redirect("staff_list")


@login_required
def unarchive_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.is_archieved = False
    user.save()
    return redirect("archived_student_list")


@login_required
def unarchive_staff(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.is_archieved = False
    user.save()
    return redirect("archived_staff_list")


@login_required
def archived_student_list(request):
    users = CustomUser.objects.filter(is_archieved=True)
    return render(request, "website/archived_student_list.html", {"users": users})


@login_required
def archived_staff_list(request):
    users = CustomUser.objects.filter(is_archieved=True)
    return render(request, "website/archived_staff_list.html", {"users": users})


@login_required
def edit_user(request, uuid):
    try:
        user = get_object_or_404(CustomUser, id=uuid)

        if request.method == "POST":
            user.email = request.POST.get("email", user.email)
            user.first_name = request.POST.get("first_name", user.first_name)
            user.last_name = request.POST.get("last_name", user.last_name)
            user.phone_number = request.POST.get("phone_number", user.phone_number)
            user.balance = request.POST.get("balance", user.balance)

            if request.user == user:
                user.is_admin = True
                user.is_staff = True
            else:
                user.is_staff = request.POST.get("is_staff") == "on"
                user.is_admin = request.POST.get("is_admin") == "on"

            user.save()
            return redirect("staff_list" if user.is_staff else "student_list")

        return render(request, "website/edit_user.html", {"user": user})
    except Exception as e:
        return HttpResponseBadRequest(f"Error editing user: {str(e)}")
