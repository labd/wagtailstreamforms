from django.db import models

from wagtailstreamforms.models import AbstractFormSetting


class ValidFormSettingsModel(AbstractFormSetting):
    name = models.CharField(max_length=255)
    number = models.IntegerField()


class InvalidFormSettingsModel(models.Model):
    pass
