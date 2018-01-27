import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtailstreamforms.blocks import WagtailFormBlock
from wagtailstreamforms.models import AbstractFormSubmission, BaseForm


class ExampleForm(BaseForm):

    def get_data_fields(self):
        data_fields = super().get_data_fields()
        data_fields += [
            ('user', _('User')),
            ('page', _('Page'))
        ]
        return data_fields

    def get_submission_class(self):
        return ExampleFormSubmission

    def process_form_submission(self, form):
        if self.store_submission:
            self.get_submission_class().objects.create(
                form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
                form=self,
                page=form.page,
                user=form.user if not form.user.is_anonymous() else None
            )


class ExampleFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)

    def get_data(self):
        form_data = super().get_data()
        form_data.update({
            'page': self.page,
            'user': self.user
        })
        return form_data


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
