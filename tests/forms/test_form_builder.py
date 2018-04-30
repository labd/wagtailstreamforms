from django import forms

from wagtailstreamforms.forms import FormBuilder
from wagtailstreamforms.models import Form, FormField

from ..test_case import AppTestCase


class FormBuilderTests(AppTestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.form = Form.objects.get(pk=1)
        self.field = FormField.objects.create(
            form=self.form,
            label='My field',
            field_type='singleline'
        )

    def test_field_exists(self):
        fb = FormBuilder(self.form.get_form_fields())
        form_class = fb.get_form_class()
        field_names = form_class.base_fields.keys()
        self.assertIn('my-field', field_names)
        self.assertIsInstance(form_class.base_fields['my-field'], forms.CharField)

    # TODO: more tests once we refactor the FormField model
