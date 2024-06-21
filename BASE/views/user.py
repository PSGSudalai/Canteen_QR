# BASE/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from BASE.models import CustomUser


def signup_view(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(
                request, "Username already exists. Please choose another username."
            )

        elif CustomUser.objects.filter(email=email).exists():
            messages.error(
                request, "Email address is already in use. Please use another email."
            )

        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=firstname,
                last_name=lastname,
            )
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect("home")

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
            return redirect("signin")

    return render(request, "registration/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout
