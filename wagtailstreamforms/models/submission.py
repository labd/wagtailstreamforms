import json

from django.db import models
from django.utils.translation import gettext_lazy as _


class FormSubmission(models.Model):
    """Data for a form submission."""

    form_data = models.TextField(_("Form data"))
    form = models.ForeignKey("Form", verbose_name=_("Form"), on_delete=models.CASCADE)
    submit_time = models.DateTimeField(_("Submit time"), auto_now_add=True)

    def get_data(self):
        """Returns dict with form data."""
        form_data = json.loads(self.form_data)

        form_data.update({"submit_time": self.submit_time})

        return form_data

    def __str__(self):
        return self.form_data

    class Meta:
        ordering = ["-submit_time"]
        verbose_name = _("Form submission")
