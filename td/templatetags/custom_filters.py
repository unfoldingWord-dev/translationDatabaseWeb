from __future__ import absolute_import

from django import template
from django.template.defaultfilters import stringfilter

from ..gl_tracking.models import GLDirector


register = template.Library()


@register.filter(name="append_qs")
def append_qs(list_1, list_2):
    print "RETURNING", list(set(list(list_1) + list(list_2)))
    return list(set(list(list_1) + list(list_2)))


@register.filter(name="bible_status")
@stringfilter
def bible_status(value):
    """
    Returns the status of Bible Translation according to Joshua Project
    """
    return {
        "": "-",
        "0": "questionable need",
        "1": "none, definite need",
        "2": "portions completed",
        "3": "NT completed",
        "4": "complete Bible",
    }[value]


@register.filter(name="lang_status")
@stringfilter
def lang_status(value):
    """
    Returns the status of a language according to Joshua Project
    """
    return {
        "": "-",
        "L": "living",
        "N": "nearly extinct",
    }[value]


@register.filter(name="percents")
@stringfilter
def percents(value):
    """
    Appends a percentage sign
    """
    return ' '.join([value, '%']) if value else "-"


@register.filter(name='is_super_gl_director')
def is_super_gl_director(user):
    """
    Checks if the user is a GL director supervisor
    """
    return user.username in GLDirector.super_gl_directors()
