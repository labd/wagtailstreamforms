from urllib.parse import urlencode

from django.template import Library
from django.utils.safestring import mark_safe

from wagtailstreamforms.blocks import WagtailFormBlock
from wagtailstreamforms.models import Form

register = Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """will append kwargs to the existing url replacing any passed in"""

    query = context["request"].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.simple_tag(takes_context=True)
def streamforms_form(context, slug, reference, action=".", **kwargs):
    """
    Renders a form on the page.

    {% load streamforms_tags %}
    {% streamforms_form "the-form-slug" "some-unique-reference" "." %}
    """

    try:
        form = Form.objects.get(slug=slug)

        block = WagtailFormBlock()

        # the context is a RequestContext, we need to turn it into a dict or
        # the blocks in wagtail will start to fail with dict(context)
        return block.render(
            block.to_python({"form": form.pk, "form_action": action, "form_reference": reference}),
            context.flatten(),
        )

    except Form.DoesNotExist:
        return mark_safe("")
