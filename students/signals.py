from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from random import sample
from . models import Student
from sms.utils import send_sms_student


@receiver(post_save, sender=Student)
def create_user(sender, instance, created, **kwargs):
    if created:
        temporal_pin = ''.join(sample("0123456789", 5))
        instance.temporal_pin = temporal_pin
        user = User.objects.get_or_create(username=instance.student_id)[0]
        user.student = instance
        user.set_password(temporal_pin)
        user.last_name = instance.surname
        user.first_name = instance.other_names
        user.save()
        instance.save()

        send_sms_student(temporal_pin, instance.sms_number,
                         instance.student_id)


@receiver(post_delete, sender=Student)
def delete_user(sender, instance, **kwargs):
    if hasattr(instance, "user") and instance.user:
        instance.user.delete()
