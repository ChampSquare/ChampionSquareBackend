from django import template

register = template.Library()

@register.filter
def to_alphabet(value):
    return chr(65+value) # value of 65 in char is 'A'