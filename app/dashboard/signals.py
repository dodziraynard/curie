from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Student


@receiver(post_save, sender=Student)
def create_student(sender, instance, created, **kwargs):
    if not instance.promotion_histories.exists() and instance.klass:
        instance.promote(0)


@receiver(post_delete, sender=Student)
def delete_promotion_history(sender, instance, created, **kwargs):
    instance.promotion_histories.delete()
