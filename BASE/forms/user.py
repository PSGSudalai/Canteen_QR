from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from BASE.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "phone_number")


class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
