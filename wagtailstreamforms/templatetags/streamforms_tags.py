from urllib.parse import urlencode

from django.template import Library
from django.utils.safestring import mark_safe

from wagtailstreamforms.blocks import WagtailFormBlock
from wagtailstreamforms.models import BaseForm

register = Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """ will append kwargs to the existing url replacing any passed in """

    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.simple_tag(takes_context=True)
def streamforms_form(context, slug, reference, action='.', **kwargs):
    """
    Renders a form on the page.

    {% load streamforms_tags %}
    {% streamforms_form "the-form-slug" "some-unique-reference" "." %}
    """

    form = BaseForm.objects.filter(slug=slug).first()

    if not form:
        return mark_safe('')

    block = WagtailFormBlock()

    # take what context we need for the form
    block_context = {
        'invalid_stream_form_reference': context.get('invalid_stream_form_reference'),
        'invalid_stream_form': context.get('invalid_stream_form'),
        'csrf_token': context.get('csrf_token')
    }

    return block.render(block.to_python({
        'form': form.pk,
        'form_action': action,
        'form_reference': reference
    }), block_context)
