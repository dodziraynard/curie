from pickle import TRUE
from random import sample
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
    get_pin = lambda: "".join(
        sample(list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])), 5))
    username = models.CharField(max_length=30, unique=True)
    surname = models.CharField(max_length=30, null=True, blank=True)
    other_names = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, unique=True,null=True,blank=True) #yapf: disable
    title = models.CharField(max_length=20,default="", blank=True) #yapf: disable
    photo = models.ImageField(upload_to='users', blank=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    temporal_pin = models.CharField(max_length=10, null=True, blank=True)

    activated = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = 'username'

    def get_title(self):
        group = self.groups.first()
        if group: return group.name
        return "Staff"

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return "/static/images/default_profile.jpg"

    def get_name(self):
        if self.surname and self.other_names and self.title:
            return f"{self.title.title()} {self.surname.title()} {self.other_names.title()}"
        return self.username.split('@')[0].title()
