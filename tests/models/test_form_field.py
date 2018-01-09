from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.wagtailforms.models import AbstractFormField

from wagtailstreamforms.models import BaseForm, FormField
from wagtailstreamforms.models.form_field import get_form_field_choices
from wagtailstreamforms.models.validators import RegexFieldValidator

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(FormField, AbstractFormField))


class ModelFieldTests(AppTestCase):

    def test_field_type(self):
        field = self.get_field(FormField, 'field_type')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 16)
        self.assertEqual(field.choices, get_form_field_choices())

    def test_regex_validator(self):
        field = self.get_field(FormField, 'regex_validator')
        self.assertModelPKField(field, RegexFieldValidator, models.PROTECT, True, True)

    def test_custom_css_class(self):
        field = self.get_field(FormField, 'custom_css_class')
        self.assertModelField(field, models.CharField, False, True)
        self.assertEqual(field.max_length, 255)

    def test_form(self):
        field = self.get_field(FormField, 'form')
        self.assertEqual(field.__class__, ParentalKey)
        self.assertEqual(field.remote_field.model, BaseForm)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.remote_field.related_name, 'form_fields')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
