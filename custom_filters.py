from django import template

register = template.Library()

@register.filter(name='range')
def custom_range(start, end):
    return range(start, end)
