import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager
from modelcluster.models import ClusterableModel
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    TabbedInterface,
    ObjectList
)

from .partials import EmailPartial
from .submission import FormSubmission
from wagtail_streamforms.conf import settings
from wagtail_streamforms.forms import FormBuilder
from wagtail_streamforms.utils import recaptcha_enabled


class BaseForm(ClusterableModel):
    name = models.CharField(
        max_length=255
    )
    template_name = models.CharField(
        verbose_name='template',
        max_length=255,
        choices=settings.WAGTAIL_STREAMFORMS_FORM_TEMPLATES
    )
    submit_button_text = models.CharField(
        max_length=100,
        default='Submit'
    )
    store_submission = models.BooleanField(
        default=False
    )
    add_recaptcha = models.BooleanField(
        default=False,
        help_text=_('Add a reCapcha field to the form.')
    )
    success_message = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('An optional success message to show when the form has been successfully submitted')
    )

    settings_panels = [
        FieldPanel('name', classname='full'),
        FieldPanel('template_name'),
        FieldPanel('submit_button_text'),
        FieldPanel('success_message', classname='full'),
        FieldPanel('store_submission'),
    ]

    field_panels = [
        InlinePanel('form_fields', label='Fields'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(settings_panels, heading='General'),
        ObjectList(field_panels, heading='Fields'),
    ])

    objects = InheritanceManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = _('form')

    def get_form_fields(self):
        return self.form_fields.all()

    def get_data_fields(self):
        data_fields = [('submit_time', _('Submission date')), ]
        data_fields += [(field.clean_name, field.label) for field in self.get_form_fields()]
        return data_fields

    def get_form_class(self):
        fb = FormBuilder(self.form_fields.all(), add_recaptcha=self.add_recaptcha)
        return fb.get_form_class()

    def get_form_parameters(self):
        return {}

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        form_params = self.get_form_parameters()
        form_params.update(kwargs)
        return form_class(*args, **form_params)

    def process_form_submission(self, form):
        if self.store_submission:
            FormSubmission.objects.create(
                form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
                form=self
            )


if recaptcha_enabled():
    BaseForm.field_panels.insert(0, FieldPanel('add_recaptcha'))


class BasicForm(BaseForm):
    pass


class EmailForm(BaseForm, EmailPartial):

    edit_handler = TabbedInterface([
        ObjectList(BaseForm.settings_panels, heading='General'),
        ObjectList(BaseForm.field_panels, heading='Fields'),
        ObjectList(EmailPartial.panels, heading='Email Submission'),
    ])

    def process_form_submission(self, form):
        super(EmailForm, self).process_form_submission(form)
        self.send_form_mail(form)
