from django.db import models
from django.utils.translation import ugettext_lazy as _


class FormSubmissionFile(models.Model):
    """ Data for a form submission file. """

    submission = models.ForeignKey(
        'FormSubmission',
        verbose_name=_('Submission'),
        on_delete=models.CASCADE,
        related_name='files'
    )
    field = models.CharField(
        verbose_name=_('Field'),
        max_length=255
    )
    file = models.FileField(
        verbose_name=_('File'),
        upload_to='streamforms/'
    )

    def __str__(self):
        return self.file.name

    class Meta:
        ordering = ['field', 'file']
        verbose_name = _('Form submission file')

    @property
    def url(self):
        return self.file.url
