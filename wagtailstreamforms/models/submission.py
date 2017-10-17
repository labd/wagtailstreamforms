import json

from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractFormSubmission(models.Model):
    """
    Data for a form submission.

    You can create custom submission model based on this abstract model.
    For example, if you need to save additional data or a reference to a user.
    """

    form_data = models.TextField()
    form = models.ForeignKey(
        'wagtailstreamforms.BaseForm',
        on_delete=models.CASCADE
    )
    submit_time = models.DateTimeField(
        verbose_name=_('submit time'),
        auto_now_add=True
    )

    def get_data(self):
        """
        Returns dict with form data.

        You can override this method to add additional data.
        """
        form_data = json.loads(self.form_data)

        form_data.update(
            {'submit_time': self.submit_time, }
        )

        return form_data

    def __str__(self):
        return self.form_data

    class Meta:
        abstract = True
        ordering = ['-submit_time', ]
        verbose_name = _('form submission')


class FormSubmission(AbstractFormSubmission):
    """ Data for a Form submission. """
