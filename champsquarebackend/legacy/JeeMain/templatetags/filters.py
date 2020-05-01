from django import template

register = template.Library()


@register.filter
def leading_zeros(value, desired_digits):
    return str(value).zfill(desired_digits)