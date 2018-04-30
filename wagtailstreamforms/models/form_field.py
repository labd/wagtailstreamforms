from django.db import models
from django.utils.text import capfirst, slugify
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey
from unidecode import unidecode
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Orderable

from wagtailstreamforms import fields


def get_field_type_choices():
    choices = tuple()
    for k, v in fields.get_fields().items():
        choices += ((k, capfirst(k)), )
    return choices


class FormField(Orderable):
    """ Database Fields required for building a Django Form field. """

    label = models.CharField(
        verbose_name=_('label'),
        max_length=255,
        help_text=_('The label of the form field')
    )
    field_type = models.CharField(
        _('Field type'),
        max_length=16,
        choices=get_field_type_choices()
    )
    form = ParentalKey(
        'Form',
        verbose_name=_('Form'),
        on_delete=models.CASCADE,
        related_name='form_fields'
    )
    required = models.BooleanField(
        verbose_name=_('required'),
        default=True
    )
    choices = models.TextField(
        verbose_name=_('choices'),
        blank=True,
        help_text=_('Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.')
    )
    default_value = models.CharField(
        verbose_name=_('default value'),
        max_length=255,
        blank=True,
        help_text=_('Default value. Comma separated values supported for checkboxes.')
    )
    help_text = models.CharField(
        verbose_name=_('help text'),
        max_length=255,
        blank=True
    )

    @property
    def clean_name(self):
        return str(slugify(str(unidecode(self.label))))

    panels = [
        FieldPanel('label'),
        FieldPanel('help_text'),
        FieldPanel('required'),
        FieldPanel('field_type', classname="formbuilder-type"),
        FieldPanel('choices', classname="formbuilder-choices"),
        FieldPanel('default_value', classname="formbuilder-default"),
    ]

    class Meta:
        ordering = ['sort_order']
