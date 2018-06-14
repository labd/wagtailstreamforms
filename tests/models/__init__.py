from django.db import models

from wagtailstreamforms.models import AbstractFormSetting


class ValidFormSettingsModel(AbstractFormSetting):
    name = models.CharField(max_length=255)


class InvalidFormSettingsModel(models.Model):
    pass
