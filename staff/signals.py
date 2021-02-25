from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from random import sample
from . models import Staff
from sms.utils import send_sms_staff
from django.db import transaction
from logger.utils import log_system_error


@receiver(post_save, sender=Staff)
def create_user(sender, instance, created, **kwargs):
    if created:
        temporal_pin = ''.join(sample("0123456789", 5))
        instance.temporal_pin = temporal_pin
        user = User.objects.get_or_create(username=instance.staff_id)[0]
        user.staff = instance
        instance.user = user
        user.set_password(temporal_pin)
        user.last_name = instance.surname
        user.first_name = instance.other_names
        user.save()
        instance.save()
        send_sms_staff(temporal_pin, instance.sms_number, instance.staff_id)


@receiver(post_delete, sender=Staff)
def delete_user(sender, instance, **kwargs):
    try:
        if hasattr(instance, "user") and instance.user:
            with transaction.atomic():
                instance.user.delete()
    except User.DoesNotExist as err:
        log_system_error("delete_staff_user_signal", str(err))
        print(err)
