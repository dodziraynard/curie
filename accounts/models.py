from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email_address = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to="accounts", null=True, blank=True)
    fullname = models.CharField(max_length=200, null=True, blank=True)
    last_login_date = models.DateTimeField(auto_now=True)
    access_via = models.CharField(max_length=20, default="mobile")
    address = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, default='Ghana')
    phone = models.CharField(max_length=20, null=True, blank=True)
    facebook = models.URLField(default="https://www.facebook.com/")
    twitter = models.URLField(default="https/www.twitter.com/")
    instagram = models.URLField(default='https://www.instagram.com/')
    linkedIn = models.URLField(default='https://www.linkedin.com/')

    # Django stuff for authentication
    USERNAME_FIELD = "username"
    objects = AccountManager()
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "users"
        permissions = [
            ("view_dashboard", "View Dashboard"),
            ("can_setup", "Setup System"),
        ]

    def get_name(self):
        return self.fullname or self.username

    def cart_items_count(self):
        total = 0
        for item in self.cart_items.all():
            total += item.quantity
        return total

    def __str__(self):
        return self.username
