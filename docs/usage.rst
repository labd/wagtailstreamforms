Basic Usage
===========

Firstly add the ``WagtailFormBlock()`` in any of your streamfields:

::

    body = StreamField([
        ...
        ('form', WagtailFormBlock())
        ...
    ])

And make sure your ``Page`` inherits from the ``StreamFormPageMixin`` mixin:

::

    class BasicPage(StreamFormPageMixin, Page):

This allows forms to be posted to the current page and processed, any validation errors will appear on the round trip.

Full example:

::

    from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
    from wagtail.wagtailcore.fields import StreamField
    from wagtail.wagtailcore.models import Page
    from wagtailstreamforms.blocks import WagtailFormBlock
    from wagtailstreamforms.models import StreamFormPageMixin


    class BasicPage(StreamFormPageMixin, Page):

        body = StreamField([
            ('form', WagtailFormBlock())
        ])

        content_panels = Page.content_panels + [
            StreamFieldPanel('body'),
        ]
