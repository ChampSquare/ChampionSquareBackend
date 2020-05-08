from django import template
from django.template.defaultfilters import stringfilter
import datetime

register = template.Library()

@stringfilter
@register.filter(name='escape_quotes')
def escape_quotes(value):
	value = value.decode("utf-8")
	escape_single_quotes = value.replace("'", "\\'")
	escape_single_and_double_quotes = escape_single_quotes.replace('"', '\\"')

	return escape_single_and_double_quotes

@register.simple_tag(name="completed")
def completed(answerpaper):
	return answerpaper.filter(status="completed").count()

@register.simple_tag(name="inprogress")
def inprogress(answerpaper):
    return answerpaper.filter(status="inprogress").count()

@register.simple_tag(name="print_timestamp")
def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = int(timestamp)
    except ValueError:
        return None
    return datetime.timedelta(milliseconds=ts)

register.filter(print_timestamp)
