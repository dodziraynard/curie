import math
from django.utils import timezone


def time_left(deadline):
    diff = deadline - timezone.now()

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        seconds = diff.seconds
        if seconds == 1:
            return str(seconds) + "second left"
        elif seconds <= 0:
            return "Deadline: {}".format(deadline.date())
        else:
            return str(seconds) + " seconds left"

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        minutes = math.floor(diff.seconds/60)

        if minutes == 1:
            return str(minutes) + " minute left"
        else:
            return str(minutes) + " minutes left"

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        hours = math.floor(diff.seconds/3600)

        if hours == 1:
            return str(hours) + " hour left"
        else:
            return str(hours) + " hours left"

    # 1 day to 30 days
    if diff.days >= 1 and diff.days < 30:
        days = diff.days

        if days == 1:
            return str(days) + " day left"
        else:
            return str(days) + " days left"

    if diff.days >= 30 and diff.days < 365:
        months = math.floor(diff.days/30)
        if months == 1:
            return str(months) + " month left"
        else:
            return str(months) + " months left"

    if diff.days >= 365:
        years = math.floor(diff.days/365)
        if years == 1:
            return str(years) + " year left"
        else:
            return str(years) + " years left"
