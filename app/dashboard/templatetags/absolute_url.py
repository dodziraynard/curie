from django import template
from django.shortcuts import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def absolute_url(context, relative_url, *args, **kwargs):
    request = context['request']
    return request.build_absolute_uri(relative_url)
