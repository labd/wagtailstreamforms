from django import forms
from wagtailstreamforms import fields
from wagtailstreamforms.models import FormField
from ..test_case import AppTestCase


class TestBaseField(AppTestCase):

    def test_options(self):
        class MyField(fields.BaseField):
            field_class = forms.CharField

        instance = FormField(
            label='My Field',
            required=True,
            default_value='Value',
            help_text='Help'
        )

        options = MyField().get_options(instance)

        self.assertEqual(options['label'], instance.label)
        self.assertEqual(options['required'], instance.required)
        self.assertEqual(options['initial'], instance.default_value)
        self.assertEqual(options['help_text'], instance.help_text)

    def test_no_form_class_raises_exception(self):
        class MyField(fields.BaseField):
            field_class = None

        with self.assertRaises(NotImplementedError) as ex:
            MyField().get_formfield({})
        the_exception = ex.exception

        self.assertEqual(the_exception.args[0], 'must provide a cls.field_class')

    def test_formfield(self):
        class MyField(fields.BaseField):
            field_class = forms.CharField

        instance = FormField(
            label='My Field',
            required=True,
            default_value='Value',
            help_text='Help'
        )

        field = MyField().get_formfield(instance)

        self.assertIsInstance(field, forms.CharField)

        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.initial, instance.default_value)
        self.assertEqual(field.help_text, instance.help_text)
