from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtailstreamforms.blocks import WagtailFormBlock


class BasicPage(Page):

    body = StreamField([
        ('rich_text', blocks.RichTextBlock()),
        ('form', WagtailFormBlock())
    ])

    # show in menu ticked by default
    show_in_menus_default = True

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
