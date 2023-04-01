import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('lms')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


def celery_info():
    return bool(app.control.inspect().active())
