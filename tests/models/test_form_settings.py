from django.db import models
from wagtailstreamforms.models import AbstractFormSetting, Form

from ..test_case import AppTestCase
from . import ValidFormSettingsModel


class ModelGenericTests(AppTestCase):
    fixtures = ["test"]

    def test_abstract(self):
        self.assertTrue(AbstractFormSetting._meta.abstract)

    def test_str(self):
        model = ValidFormSettingsModel(form=Form.objects.get(pk=1))
        self.assertEqual(model.__str__(), model.form.title)


class ModelFieldTests(AppTestCase):
    def test_form(self):
        field = self.get_field(AbstractFormSetting, "form")
        self.assertModelField(field, models.OneToOneField)
        self.assertEqual(field.remote_field.model, "wagtailstreamforms.Form")
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.remote_field.related_name, "advanced_settings")
