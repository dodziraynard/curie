from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Account


@receiver(post_save, sender=User)
def on_create_user(sender, instance, created, **kwargs):
    if not hasattr(instance, "account"):
        Account.objects.create(user=instance)
