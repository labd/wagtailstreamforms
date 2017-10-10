from django.db import models

from wagtail_streamforms.models import RegexFieldValidator

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(RegexFieldValidator, models.Model))

    def test_str(self):
        model = RegexFieldValidator(name="foo")
        self.assertEquals(model.__str__(), model.name)

    def test_ordering(self):
        self.assertEqual(RegexFieldValidator._meta.ordering, ['name', ])


class ModelFieldTests(AppTestCase):

    def test_name(self):
        field = self.get_field(RegexFieldValidator, 'name')
        self.assertModelField(field, models.CharField)
        self.assertEquals(field.max_length, 255)

    def test_description(self):
        field = self.get_field(RegexFieldValidator, 'description')
        self.assertModelField(field, models.TextField, True, True)

    def test_regex(self):
        field = self.get_field(RegexFieldValidator, 'regex')
        self.assertModelField(field, models.TextField)

    def test_error_message(self):
        field = self.get_field(RegexFieldValidator, 'error_message')
        self.assertModelField(field, models.CharField)
        self.assertEquals(field.max_length, 255)
