from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class AccountManager(BaseUserManager):
    """
    Custom user model manager where username is the unique identifiers
    for authentication instead of username.
    """
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('The username must be set'))
        photo = extra_fields.pop("photo", None)
        user = self.model(username=username, **extra_fields)
        if photo:
            user.photo = photo[0]
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)