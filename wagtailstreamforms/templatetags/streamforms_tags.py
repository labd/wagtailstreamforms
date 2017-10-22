from urllib.parse import urlencode

from django.template import Library


register = Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """ will append kwargs to the existing url replacing any passed in """

    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
