from django.db import models
from django.test import TestCase

class AppTestCase(TestCase):

    def get_field(self, modelClass, name):
        return modelClass._meta.get_field(name)

    _non_blankable_fields = [
        models.BooleanField
    ]

    def assertModelField(self, field, expected_class, null=False, blank=False, default=None):
        self.assertEqual(field.__class__, expected_class)
        self.assertEqual(field.null, null)
        if expected_class not in self._non_blankable_fields:
            self.assertEqual(field.blank, blank)

        if default:
            self.assertEqual(field.default, default)

    def assertModelDecimalField(self, field, max_digits, decimal_places, null=False, blank=False):
        self.assertEqual(field.__class__, models.DecimalField)
        self.assertEqual(field.max_digits, max_digits)
        self.assertEqual(field.decimal_places, decimal_places)
        self.assertEqual(field.null, null)
        self.assertEqual(field.blank, blank)

    def assertModelPKField(self, field, rel_to, on_delete, null=False, blank=False, related_name=None):
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertEqual(field.rel.to, rel_to)
        self.assertEqual(field.rel.on_delete, on_delete)
        self.assertEqual(field.null, null)
        self.assertEqual(field.blank, blank)

        if related_name:
            self.assertEqual(field.rel.related_name, related_name)
