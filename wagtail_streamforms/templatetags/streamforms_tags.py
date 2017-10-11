from django import template


register = template.Library()


@register.assignment_tag
def define(val=None):
    return val
