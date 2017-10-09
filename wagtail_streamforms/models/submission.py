import json

from django.db import models
from django.utils.translation import ugettext_lazy as _


class FormSubmission(models.Model):

    form_data = models.TextField()
    form = models.ForeignKey(
        'BaseForm',
        on_delete=models.CASCADE
    )
    submit_time = models.DateTimeField(
        verbose_name=_('submit time'),
        auto_now_add=True
    )

    def get_data(self):
        form_data = json.loads(self.form_data)
        form_data.update({'submit_time': self.submit_time, })
        return form_data

    def __str__(self):
        return self.form_data

    class Meta:
        ordering = ['-submit_time', ]
        verbose_name = _('form submission')
