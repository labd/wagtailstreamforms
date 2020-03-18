from django import forms
from wagtailstreamforms import fields

from ..test_case import AppTestCase


class TestBaseField(AppTestCase):
    def test_options(self):
        class MyField(fields.BaseField):
            field_class = forms.CharField

        data = {
            "label": "field",
            "required": True,
            "default_value": "default",
            "help_text": "help",
        }

        options = MyField().get_options(data)

        self.assertEqual(options["label"], data["label"])
        self.assertEqual(options["required"], data["required"])
        self.assertEqual(options["initial"], data["default_value"])
        self.assertEqual(options["help_text"], data["help_text"])

    def test_no_form_class_raises_exception(self):
        class MyField(fields.BaseField):
            field_class = None

        with self.assertRaises(NotImplementedError) as ex:
            MyField().get_formfield({})
        the_exception = ex.exception

        self.assertEqual(the_exception.args[0], "must provide a cls.field_class")

    def test_formfield(self):
        class MyField(fields.BaseField):
            field_class = forms.CharField

        data = {
            "label": "field",
            "required": True,
            "default_value": "default",
            "help_text": "help",
        }

        field = MyField().get_formfield(data)

        self.assertIsInstance(field, forms.CharField)

        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.initial, data["default_value"])
        self.assertEqual(field.help_text, data["help_text"])
