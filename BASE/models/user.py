# BASE/models/user.py

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from BASE.models import BaseModels


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModels):
    user_id = models.CharField(max_length=30, unique=True, editable=False, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)
    is_user = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["first_name", "last_name"]

    def save(self, *args, **kwargs):
        if not self.user_id:
            last_user = CustomUser.objects.order_by("-id").first()
            if last_user and last_user.user_id:
                last_user_id_int = int(last_user.user_id[1:])
                new_user_id_int = last_user_id_int + 1
                self.user_id = f"R{new_user_id_int:03d}"
            else:
                self.user_id = "R001"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
