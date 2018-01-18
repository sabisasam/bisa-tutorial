from django import template
from django.template.defaultfilters import stringfilter

from fortune.models import Fortune

register = template.Library()


@register.filter
@stringfilter
def fortune(category):
    """
    Returns a fortune of given category.
    Usage: {{ "category" | fortune }}
    """
    return Fortune.fortune(category.lower())


@register.simple_tag
def fortune():
    """
    Returns a random fortune.
    Usage: {% fortune %}
    """
    return Fortune.fortune()
