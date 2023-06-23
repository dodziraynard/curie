import decimal
from random import sample

import geocoder
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManger(BaseUserManager):
    """Define a model manager for User model"""

    def _create_user(self, username, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not username:
            raise ValueError('The given email must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    def get_pin():
        return "".join(
            sample(list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])), 4))

    username = models.CharField(max_length=30, unique=True)
    surname = models.CharField(max_length=30, null=True, blank=True)
    other_names = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=10,null=True,blank=True) #yapf: disable
    title = models.CharField(max_length=20,default="", blank=True) #yapf: disable
    photo = models.ImageField(upload_to='users', blank=True)
    signature = models.ImageField(upload_to='signatures',
                                  null=True,
                                  blank=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    temporal_pin = models.CharField(max_length=10, default=get_pin)
    dob = models.DateTimeField(null=True, blank=True)

    activated = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    changed_password = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = 'username'

    class Meta:
        permissions = [
            ('reset_password', 'Can reset user password'),
        ]

    def model_name(self):
        return self.__class__.__name__.lower()

    def signature_url(self):
        if self.signature:
            return self.signature.url
        return ""

    def get_title(self):
        group = self.groups.first()
        if group: return group.name
        return "Staff"

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return "/static/images/default_profile.jpg"

    def get_name(self):
        if self.surname and self.other_names:
            return f"{self.surname.title()} {self.other_names.title()}"
        return self.username.split('@')[0].upper()

    def save(self, *args, **kwargs):
        if self.gender:
            self.gender = self.gender.lower()
        if self.title:
            self.title = self.title.lower()
        return super().save(*args, **kwargs)


#yapf: disable
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    available_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    main_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def balance(self):
        return self.main_balance

    @property
    def amount_payable(self):
        return self.main_balance * -1

    def reset_balance(self, amount):
        self.available_balance = decimal.Decimal(amount)
        self.main_balance = decimal.Decimal(amount)
        self.save()

    def credit_account(self, amount):
        self.available_balance += decimal.Decimal(amount)
        self.main_balance += decimal.Decimal(amount)
        self.save()

class ActivityLog(models.Model):
    username = models.CharField(max_length=100)
    action = models.TextField()
    ip = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "%s %s" % (self.username, self.action)

    def get_latlng(self):
        return geocoder.ip(self.registration_ip).latlng
