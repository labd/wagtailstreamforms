Basic Usage
===========

Firstly add the ``wagtailstreamforms.blocks.WagtailFormBlock()`` in any of your streamfields:

.. code-block:: python

    body = StreamField([
        ...
        ('form', WagtailFormBlock())
        ...
    ])

And make sure your ``Page`` inherits from the ``StreamFormPageMixin`` mixin:

.. code-block:: python

    class BasicPage(StreamFormPageMixin, Page):

This allows forms to be posted to the current page and processed, any validation errors will appear on the round trip.

Example:

.. code-block:: python

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
