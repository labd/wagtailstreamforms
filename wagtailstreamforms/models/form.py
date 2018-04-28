import uuid
from copy import deepcopy

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    TabbedInterface,
    ObjectList,
    PageChooserPanel,
    MultiFieldPanel
)

from wagtailstreamforms import hooks
from wagtailstreamforms.conf import get_setting
from wagtailstreamforms.fields import HookSelectField
from wagtailstreamforms.forms import FormBuilder

from .submission import FormSubmission


class Form(ClusterableModel):
    """ A form base class, any form should inherit from this. """

    name = models.CharField(
        _('Name'),
        max_length=255
    )
    slug = models.SlugField(
        _('Slug'),
        allow_unicode=True,
        max_length=255,
        unique=True,
        help_text=_('Used to identify the form in template tags')
    )
    template_name = models.CharField(
        _('Template'),
        max_length=255,
        choices=get_setting('FORM_TEMPLATES')
    )
    submit_button_text = models.CharField(
        _('Submit button text'),
        max_length=100,
        default='Submit'
    )
    success_message = models.CharField(
        _('Success message'),
        blank=True,
        max_length=255,
        help_text=_('An optional success message to show when the form has been successfully submitted')
    )
    error_message = models.CharField(
        _('Error message'),
        blank=True,
        max_length=255,
        help_text=_('An optional error message to show when the form has validation errors')
    )
    post_redirect_page = models.ForeignKey(
        'wagtailcore.Page',
        verbose_name=_('Post redirect page'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text=_('The page to redirect to after a successful submission')
    )
    process_form_submission_hooks = HookSelectField(
        blank=True
    )

    settings_panels = [
        FieldPanel('name', classname='full'),
        FieldPanel('slug'),
        FieldPanel('template_name'),
        FieldPanel('submit_button_text'),
        MultiFieldPanel([
            FieldPanel('success_message'),
            FieldPanel('error_message'),
        ], _('Messages')),
        FieldPanel('process_form_submission_hooks', classname='choice_field'),
        PageChooserPanel('post_redirect_page')
    ]

    field_panels = [
        InlinePanel('form_fields', label=_('Fields')),
    ]

    edit_handler = TabbedInterface([
        ObjectList(settings_panels, heading=_('General')),
        ObjectList(field_panels, heading=_('Fields')),
    ])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')

    def copy(self):
        """ Copy this form and its fields. """

        form_copy = deepcopy(self)
        form_copy.pk = None
        form_copy.slug = uuid.uuid4()
        form_copy.save()

        for field in self.form_fields.all():
            form_field_copy = deepcopy(field)
            form_field_copy.pk = None
            form_field_copy.form = form_copy
            form_field_copy.save()

        return form_copy

    copy.alters_data = True

    def get_data_fields(self):
        """ Returns a list of tuples with (field_name, field_label). """

        data_fields = [
            ('submit_time', _('Submission date')),
        ]
        data_fields += [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]

        return data_fields

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        form_params = self.get_form_parameters()
        form_params.update(kwargs)

        return form_class(*args, **form_params)

    def get_form_class(self):
        return FormBuilder(self.get_form_fields()).get_form_class()

    def get_form_fields(self):
        """ Returns the list of form fields. """

        return self.form_fields.all()

    def get_form_parameters(self):
        return {}

    def get_submission_class(self):
        """ Returns submission class. """

        return FormSubmission

    def process_form_submission(self, form):
        """ Runs each hook if selected in the form. """

        for fn in hooks.get_hooks('process_form_submission'):
            if fn.__name__ in self.process_form_submission_hooks:
                fn(self, form)
