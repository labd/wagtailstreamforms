from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail_streamforms.blocks import WagtailFormBlock
from wagtail_streamforms.models import StreamFormPageMixin


class BasicPage(StreamFormPageMixin, Page):

    body = StreamField([
        ('form', WagtailFormBlock())
    ])

    # show in menu ticked by default
    show_in_menus_default = True

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
