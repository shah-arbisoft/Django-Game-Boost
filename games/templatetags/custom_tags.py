"""Creating Custom tags"""
from django import template

register = template.Library()


@register.simple_tag
def alias(obj):
    """
    Custom tag to update values of a variable inside a template
    """
    return obj
