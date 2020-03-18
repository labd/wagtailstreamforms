from django.db import models


class AbstractFormSetting(models.Model):
    form = models.OneToOneField(
        "wagtailstreamforms.Form",
        on_delete=models.CASCADE,
        related_name="advanced_settings",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.form.title
