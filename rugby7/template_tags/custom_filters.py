from django import template
from django.utils.dateparse import parse_datetime

register = template.Library()

@register.filter
def date_only(value):
    return value.date() if value else value
