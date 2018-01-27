from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel


class RegexFieldValidator(models.Model):
    """ Regex validation data for a regex validated form field. """

    name = models.CharField(
        _('Name'),
        max_length=255
    )
    description = models.TextField(
        _('Description'),
        null=True,
        blank=True
    )
    regex = models.TextField(
        _('Regex')
    )
    error_message = models.CharField(
        _('Error message'),
        max_length=255
    )

    panels = [
        FieldPanel('name', classname='full'),
        FieldPanel('description', classname='full'),
        FieldPanel('regex', classname='full'),
        FieldPanel('error_message', classname='full'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = _('Regex validator')
        verbose_name_plural = _('Regex validators')
