from django import forms
from wagtailstreamforms import fields
from ..test_case import AppTestCase


class MyField(fields.BaseField):
    field_class = forms.CharField


class TestFieldRegistering(AppTestCase):

    @classmethod
    def setUpClass(cls):
        fields.register('myfield', MyField)

    @classmethod
    def tearDownClass(cls):
        del fields._fields['myfield']

    def test_field(self):
        self.assertIn('myfield', fields.get_fields())
