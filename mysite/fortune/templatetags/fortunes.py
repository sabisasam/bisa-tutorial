from django import template
from django.template.defaultfilters import stringfilter

from fortune.models import Fortune

register = template.Library()


@register.filter
@stringfilter
def fortune(pack):
    """
    :param pack:
    """
    response = Fortune.fortune()
    return (response)


@register.simple_tag
def fortune():
    """
    """
    return Fortune.fortune()
