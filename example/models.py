from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtailstreamforms.blocks import WagtailFormBlock
from wagtailstreamforms.models import StreamFormPageMixin


class BasicPage(StreamFormPageMixin, Page):

    body = StreamField([
        ('form', WagtailFormBlock())
    ])

    # show in menu ticked by default
    show_in_menus_default = True

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
