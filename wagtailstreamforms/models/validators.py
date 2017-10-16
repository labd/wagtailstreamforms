from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel


class RegexFieldValidator(models.Model):
    """ Regex validation data for a regex validated form field. """

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    regex = models.TextField()
    error_message = models.CharField(max_length=255)

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
        verbose_name = _('regex validator')
