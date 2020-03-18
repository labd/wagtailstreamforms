from django import forms
from wagtailstreamforms import wagtailstreamforms_fields as wsf_fields
from wagtailstreamforms.models import Form

from ..test_case import AppTestCase


class TestFields(AppTestCase):
    fixtures = ["test"]

    def setUp(self):
        self.form = Form.objects.get(pk=1)

    def get_form_field_data(self, name):
        return [
            item["value"]
            for item in self.form.get_form_fields()
            if item["type"] == name
        ][0]

    def test_singleline_field(self):
        data = self.get_form_field_data("singleline")
        cls = wsf_fields.SingleLineTextField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.CharField)
        self.assertIsInstance(field.widget, forms.widgets.TextInput)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
        self.assertEqual(field.initial, data["default_value"])

    def test_multiline_field(self):
        data = self.get_form_field_data("multiline")
        cls = wsf_fields.MultiLineTextField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.CharField)
        self.assertIsInstance(field.widget, forms.widgets.Textarea)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
        self.assertEqual(field.initial, data["default_value"])

    def test_date_field(self):
        data = self.get_form_field_data("date")
        cls = wsf_fields.DateField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.DateField)
        self.assertIsInstance(field.widget, forms.widgets.DateInput)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
        self.assertEqual(field.initial, data["default_value"])

    def test_datetime_field(self):
        data = self.get_form_field_data("datetime")
        cls = wsf_fields.DateTimeField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.DateTimeField)
        self.assertIsInstance(field.widget, forms.widgets.DateTimeInput)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
        self.assertEqual(field.initial, data["default_value"])

    def test_email_field(self):
        data = self.get_form_field_data("email")
        cls = wsf_fields.EmailField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.EmailField)
        self.assertIsInstance(field.widget, forms.widgets.EmailInput)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
        self.assertEqual(field.initial, data["default_value"])

    def test_url_field(self):
        data = self.get_form_field_data("url")
        cls = wsf_fields.URLField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.URLField)
        self.assertIsInstance(field.widget, forms.widgets.URLInput)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
        self.assertEqual(field.initial, data["default_value"])

    def test_number_field(self):
        data = self.get_form_field_data("number")
        cls = wsf_fields.NumberField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.DecimalField)
        self.assertIsInstance(field.widget, forms.widgets.NumberInput)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
        self.assertEqual(field.initial, data["default_value"])

    def test_dropdown_field(self):
        data = self.get_form_field_data("dropdown")
        cls = wsf_fields.DropdownField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.ChoiceField)
        self.assertIsInstance(field.widget, forms.widgets.Select)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
        self.assertEqual(field.choices, [(c, c) for c in data["choices"]])

        data["empty_label"] = "Please Select"
        field = cls.get_formfield(data)
        self.assertEqual(field.choices[0], ("", "Please Select"))

    def test_radio_field(self):
        data = self.get_form_field_data("radio")
        cls = wsf_fields.RadioField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.ChoiceField)
        self.assertIsInstance(field.widget, forms.widgets.RadioSelect)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
        self.assertEqual(field.choices, [(c, c) for c in data["choices"]])

    def test_checkboxes_field(self):
        data = self.get_form_field_data("checkboxes")
        cls = wsf_fields.CheckboxesField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.MultipleChoiceField)
        self.assertIsInstance(field.widget, forms.widgets.CheckboxSelectMultiple)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
        self.assertEqual(field.choices, [(c, c) for c in data["choices"]])

    def test_checkbox_field(self):
        data = self.get_form_field_data("checkbox")
        cls = wsf_fields.CheckboxField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.BooleanField)
        self.assertIsInstance(field.widget, forms.widgets.CheckboxInput)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])

    def test_hidden_field(self):
        data = self.get_form_field_data("hidden")
        cls = wsf_fields.HiddenField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.CharField)
        self.assertIsInstance(field.widget, forms.widgets.HiddenInput)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
        self.assertEqual(field.initial, data["default_value"])

    def test_singlefile_field(self):
        data = self.get_form_field_data("singlefile")
        cls = wsf_fields.SingleFileField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.FileField)
        self.assertIsInstance(field.widget, forms.widgets.FileInput)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])

    def test_multifile_field(self):
        data = self.get_form_field_data("multifile")
        cls = wsf_fields.MultiFileField()
        field = cls.get_formfield(data)

        self.assertIsInstance(field, forms.FileField)
        self.assertIsInstance(field.widget, forms.widgets.FileInput)
        self.assertEqual(field.label, data["label"])
        self.assertEqual(field.required, data["required"])
        self.assertEqual(field.help_text, data["help_text"])
