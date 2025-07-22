from django import template
import calendar

register = template.Library()

@register.filter
def to(value, arg):
    return range(int(value), int(arg) + 1)

@register.filter
def get_month_name(num):
    return calendar.month_name[int(num)]