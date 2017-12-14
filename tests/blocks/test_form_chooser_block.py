from wagtailstreamforms.blocks import FormChooserBlock
from wagtailstreamforms.models import BaseForm

from ..test_case import AppTestCase


class TestFormChooserBlockTestCase(AppTestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.basic_form = BaseForm.objects.get(pk=1)
        self.email_form = BaseForm.objects.get(pk=2)

    def test_value_for_form(self):
        block = FormChooserBlock()

        self.assertEqual(block.value_for_form(self.basic_form.pk), self.basic_form.pk)
        self.assertEqual(block.value_for_form(self.basic_form), self.basic_form.pk)

    def test_value_from_form(self):
        block = FormChooserBlock()

        # possibly a bug in wagtail as not choosing a value and submitting
        # raises invalid literal for int() with base 10: ''
        self.assertIsNone(block.value_from_form(''))

        self.assertTrue(isinstance(block.value_from_form(self.basic_form.pk), self.basic_form.__class__))
        self.assertTrue(isinstance(block.value_from_form(self.basic_form), self.basic_form.__class__))

    def test_to_python(self):
        block = FormChooserBlock()

        self.assertIsNone(block.to_python(None))
        self.assertIsNone(block.to_python(100))

        self.assertTrue(isinstance(block.to_python(self.basic_form.pk), self.basic_form.__class__))

    def test_form_render(self):
        block = FormChooserBlock()

        test_form_html = block.render_form(self.basic_form, 'form')
        expected_html = '\n'.join([
            '<select name="form" placeholder="" id="form">',
            '<option value="">---------</option>',
            '<option value="%s" selected>Basic Form</option>' % self.basic_form.id,
            '<option value="%s">Email Form</option>' % self.email_form.id,
            '</select>'
        ])
        self.assertInHTML(expected_html, test_form_html)
