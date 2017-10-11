from wagtail_streamforms.blocks import FormChooserBlock
from wagtail_streamforms.models import BasicForm

from ..test_case import AppTestCase


class TestFormChooserBlockTestCase(AppTestCase):

    def setUp(self):
        self.form = BasicForm.objects.create(
            name='Some Form',
            template_name='streamforms/form_block.html'
        )

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
