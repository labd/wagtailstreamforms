from wagtailstreamforms.blocks import FormChooserBlock
from wagtailstreamforms.models import BaseForm

from ..test_case import AppTestCase


class TestFormChooserBlockTestCase(AppTestCase):

    def setUp(self):
        self.form = BaseForm.objects.create(
            name='Some Form',
            template_name='streamforms/form_block.html'
        )

    def test_value_for_form(self):
        block = FormChooserBlock()

        self.assertEquals(block.value_for_form(self.form.pk), self.form.pk)
        self.assertEquals(block.value_for_form(self.form), self.form.pk)

    def test_value_from_form(self):
        block = FormChooserBlock()

        # possibly a bug in wagtail as not choosing a value and submitting
        # raises invalid literal for int() with base 10: ''
        self.assertIsNone(block.value_from_form(''))

        self.assertTrue(isinstance(block.value_from_form(self.form.pk), self.form.__class__))
        self.assertTrue(isinstance(block.value_from_form(self.form), self.form.__class__))

    def test_to_python(self):
        block = FormChooserBlock()

        self.assertIsNone(block.to_python(None))
        self.assertIsNone(block.to_python(100))

        self.assertTrue(isinstance(block.to_python(self.form.pk), self.form.__class__))

    def test_form_render(self):
        block = FormChooserBlock()

        test_form_html = block.render_form(self.form, 'form')
        expected_html = '\n'.join([
            '<select name="form" placeholder="" id="form">',
            '<option value="">---------</option>',
            '<option value="%s" selected>Some Form</option>' % self.form.id,
            '</select>'
        ])
        self.assertInHTML(expected_html, test_form_html)
