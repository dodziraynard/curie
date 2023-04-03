"""
This module is responsible for processing files using the celery worker
"""
from celery import shared_task

from dashboard.models import Notification


@shared_task
def send_notifications_with_id_tag(id_tag):
    for notification in Notification.objects.filter(id_tag=id_tag):
        notification.send()


@shared_task
def send_notification(notification_id):
    notification = Notification.objects.filter(id=notification_id).first()
    if notification:
        notification.send()
