from django import forms
from wagtailstreamforms.fields import get_fields
from wagtailstreamforms.forms import FormBuilder
from wagtailstreamforms.models import Form

from ..test_case import AppTestCase


class FormBuilderTests(AppTestCase):
    fixtures = ["test.json"]

    def setUp(self):
        self.form = Form.objects.get(pk=1)

    def test_formfields(self):
        fields = self.form.get_form_fields()
        formfields = FormBuilder(fields).formfields
        for field in fields:
            self.assertIn(field["type"], formfields)

    def test_formfields__invalid_type(self):
        fields = [{"type": "foo", "value": {}}]
        with self.assertRaises(AttributeError) as ex:
            FormBuilder(fields).formfields
        self.assertEqual(
            ex.exception.args[0], "Could not find a registered field of type foo"
        )

    def test_formfields__missing_label_in_value(self):
        fields = [{"type": "singleline", "value": {}}]
        with self.assertRaises(AttributeError) as ex:
            FormBuilder(fields).formfields
        self.assertEqual(
            ex.exception.args[0],
            "No label value can be determined for an instance of SingleLineTextField. "
            "Add a 'label' CharBlock() in your field's get_form_block() method to allow "
            "this to be specified by form editors. Or, override get_formfield_label() "
            "to return a different value."
        )

    def test_get_form_class(self):
        fields = self.form.get_form_fields()
        form_class = FormBuilder(fields).get_form_class()

        self.assertEqual(len(form_class().fields), 16)

        formfields = form_class().fields

        for name, field in get_fields().items():
            self.assertIn(name, formfields)
            self.assertIsInstance(formfields[name], field().field_class)

        self.assertIsInstance(formfields["form_id"], forms.CharField)
        self.assertIsInstance(formfields["form_reference"], forms.CharField)
