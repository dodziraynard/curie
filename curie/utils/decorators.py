from django.shortcuts import redirect
from django.urls import reverse


def login_required(redirect_url="accounts:login"):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if (request.user.is_authenticated):
                return function(request, *args, **kwargs)
            request.session['error_message'] = "You must login first."
            referer = request.META.get('HTTP_REFERER')
            next = referer or "/"
            return redirect(reverse(redirect_url) + f"?next={next}")

        return wrapper

    return decorator
