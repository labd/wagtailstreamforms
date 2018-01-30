from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.forms.models import (
    AbstractFormField,
    FORM_FIELD_CHOICES
)


def get_form_field_choices():
    return FORM_FIELD_CHOICES + (
        ('regexfield', _('Regex validated field')),
    )


class FormField(AbstractFormField):
    """ Database Fields required for building a Django Form field. """

    field_type = models.CharField(
        _('Field type'),
        max_length=16,
        choices=get_form_field_choices()
    )
    regex_validator = models.ForeignKey(
        'RegexFieldValidator',
        verbose_name=_('Regex validator'),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text=_("Applicable only for the field type 'regex validated field'.")
    )
    form = ParentalKey(
        'BaseForm',
        verbose_name=_('Form'),
        on_delete=models.CASCADE,
        related_name='form_fields'
    )

    panels = AbstractFormField.panels + [
        FieldPanel('regex_validator'),
    ]
