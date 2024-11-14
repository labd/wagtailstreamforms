from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtailstreamforms.blocks import WagtailFormBlock
from wagtailstreamforms.models.abstract import AbstractFormSetting


class AdvancedFormSetting(AbstractFormSetting):
    to_address = models.EmailField()


class BasicPage(Page):

    body = StreamField([
        ('rich_text', blocks.RichTextBlock()),
        ('form', WagtailFormBlock())
    ])

    # show in menu ticked by default
    show_in_menus_default = True

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
