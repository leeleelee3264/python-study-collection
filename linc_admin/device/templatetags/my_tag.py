import datetime

from django import template
from django.conf import settings


register = template.Library()

@register.simple_tag
def get_settings(_key):
    return getattr(settings, _key, _key)



@register.simple_tag
def get_deliver_date(days=7):
    now = datetime.datetime.now()

    return (now + datetime.timedelta(days=days)).strftime('%Y-%m-%d')
