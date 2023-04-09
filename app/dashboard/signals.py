from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Student


@receiver(post_save, sender=Student)
def create_student(sender, instance, created, **kwargs):
    # Create history for student's initial class.
    if not instance.promotion_histories.exists() and instance.klass:
        instance.promote(0)
    
