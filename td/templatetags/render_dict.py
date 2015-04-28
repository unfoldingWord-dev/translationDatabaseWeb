from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def dict_to_dl(dictvalue, css_class="dl-horizontal"):
    result = []
    if isinstance(dictvalue, dict):
        for key, val in dictvalue.iteritems():
            result.append("<dt>{0}</dt><dd>{1}</dd>".format(key, val))
    if len(result):
        result.insert(0, '<dl class="{0}">'.format(css_class))
        result.append("</dl>")
    result_str = "".join(result)
    return mark_safe(result_str)
