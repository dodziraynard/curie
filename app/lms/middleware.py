from importlib import import_module

from django.conf import settings
from django.core.cache import cache
from ipware import get_client_ip

from accounts.models import ActivityLog
from dashboard.models.models import SystemNotification
from setup.models import School


class SingleUserSession(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Checks if different session exists for user and deletes it.
        """
        request.school = School.objects.first()
        if request.user.is_authenticated:
            cache_timeout = 86400
            cache_key = "user_pk_%s_restrict" % request.user.pk
            cache_value = cache.get(cache_key)

            if cache_value:
                if request.session.session_key != cache_value:
                    engine = import_module(settings.SESSION_ENGINE)
                    session = engine.SessionStore(session_key=cache_value)
                    session.delete()
                    cache.set(cache_key, request.session.session_key,
                              cache_timeout)
            else:
                cache.set(cache_key, request.session.session_key,
                          cache_timeout)
        return self.get_response(request)


class LogUserVisits(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Log the different pages visited by user.
        """
        path = request.path
        ignore = {"assets", "uploads", "static", "media", "api", "admin"}
        if not any(x in path.split("/") for x in ignore):
            if not settings.DEBUG:
                username = request.user.username if request.user.is_authenticated else "Anonymous"
                action = "%s %s" % (request.method, path)

                ip, _ = get_client_ip(request)
                ActivityLog.objects.create(ip=ip,
                                           username=username,
                                           action=action)
        return self.get_response(request)


class AddRequestObjects(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Log the different pages visited by user.
        """
        request.user_notifications = SystemNotification.objects.filter(
            user=request.user)
        return self.get_response(request)
