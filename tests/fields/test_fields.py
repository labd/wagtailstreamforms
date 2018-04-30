from django import forms

from wagtailstreamforms.models import FormField
from wagtailstreamforms import wagtailstreamforms_fields as wsf_fields
from ..test_case import AppTestCase


class TestFields(AppTestCase):

    def test_singleline_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='Value',
            help_text='Help',
            field_type='singleline'
        )
        cls = wsf_fields.SingleLineTextField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.CharField)
        self.assertIsInstance(field.widget, forms.widgets.TextInput)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, instance.default_value)

    def test_multiline_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='Value',
            help_text='Help',
            field_type='multiline'
        )
        cls = wsf_fields.MultiLineTextField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.CharField)
        self.assertIsInstance(field.widget, forms.widgets.Textarea)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, instance.default_value)

    def test_date_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='Value',
            help_text='Help',
            field_type='date'
        )
        cls = wsf_fields.DateField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.DateField)
        self.assertIsInstance(field.widget, forms.widgets.DateInput)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, instance.default_value)

    def test_datetime_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='Value',
            help_text='Help',
            field_type='datetime'
        )
        cls = wsf_fields.DateTimeField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.DateTimeField)
        self.assertIsInstance(field.widget, forms.widgets.DateTimeInput)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, instance.default_value)

    def test_email_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='Value',
            help_text='Help',
            field_type='email'
        )
        cls = wsf_fields.EmailField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.EmailField)
        self.assertIsInstance(field.widget, forms.widgets.EmailInput)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, instance.default_value)

    def test_url_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='Value',
            help_text='Help',
            field_type='url'
        )
        cls = wsf_fields.URLField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.URLField)
        self.assertIsInstance(field.widget, forms.widgets.URLInput)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, instance.default_value)

    def test_number_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='Value',
            help_text='Help',
            field_type='number'
        )
        cls = wsf_fields.NumberField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.DecimalField)
        self.assertIsInstance(field.widget, forms.widgets.NumberInput)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, instance.default_value)

    def test_dropdown_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='One',
            help_text='Help',
            field_type='dropdown',
            choices='One,Two,Three'
        )
        cls = wsf_fields.DropdownField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.ChoiceField)
        self.assertIsInstance(field.widget, forms.widgets.Select)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, instance.default_value)
        self.assertEqual(field.choices, [('One', 'One'), ('Two', 'Two'), ('Three', 'Three')])

    def test_multiselect_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='One,Two',
            help_text='Help',
            field_type='multiselect',
            choices='One,Two,Three'
        )
        cls = wsf_fields.MultiSelectField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.MultipleChoiceField)
        self.assertIsInstance(field.widget, forms.widgets.SelectMultiple)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, ['One', 'Two'])
        self.assertEqual(field.choices, [('One', 'One'), ('Two', 'Two'), ('Three', 'Three')])

    def test_radio_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='One',
            help_text='Help',
            field_type='radio',
            choices='One,Two,Three'
        )
        cls = wsf_fields.RadioField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.ChoiceField)
        self.assertIsInstance(field.widget, forms.widgets.RadioSelect)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, instance.default_value)
        self.assertEqual(field.choices, [('One', 'One'), ('Two', 'Two'), ('Three', 'Three')])

    def test_checkboxes_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='One,Two',
            help_text='Help',
            field_type='checkboxes',
            choices='One,Two,Three'
        )
        cls = wsf_fields.CheckboxesField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.MultipleChoiceField)
        self.assertIsInstance(field.widget, forms.widgets.CheckboxSelectMultiple)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, ['One', 'Two'])
        self.assertEqual(field.choices, [('One', 'One'), ('Two', 'Two'), ('Three', 'Three')])

    def test_checkbox_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='One',
            help_text='Help',
            field_type='checkbox'
        )
        cls = wsf_fields.CheckboxField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.BooleanField)
        self.assertIsInstance(field.widget, forms.widgets.CheckboxInput)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, instance.default_value)

    def test_hidden_field(self):
        instance = FormField(
            label='My Field',
            required=True,
            default_value='One',
            help_text='Help',
            field_type='hidden'
        )
        cls = wsf_fields.HiddenField()
        field = cls.get_formfield(instance)

        self.assertIsInstance(field, forms.CharField)
        self.assertIsInstance(field.widget, forms.widgets.HiddenInput)
        self.assertEqual(field.label, instance.label)
        self.assertEqual(field.required, instance.required)
        self.assertEqual(field.help_text, instance.help_text)
        self.assertEqual(field.initial, instance.default_value)
