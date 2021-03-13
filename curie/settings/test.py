from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'tdmavu&t#o632z(si4s&^9hiw$0v1a7i%(hm6hdjf^@jb&g1d!q'
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1"]


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# Celery
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"

# SMS
SMS_API_KEY = ""
