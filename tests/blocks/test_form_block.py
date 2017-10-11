from wagtail_streamforms.blocks import WagtailFormBlock
from wagtail_streamforms.models import BasicForm, FormField

from ..test_case import AppTestCase


class TestFormBlockTestCase(AppTestCase):

    def setUp(self):
        self.form = BasicForm.objects.create(
            name='Form',
            template_name='streamforms/form_block.html'
        )
        self.field = FormField.objects.create(
            form=self.form,
            label='name',
            field_type='singleline'
        )

    def test_render(self):
        block = WagtailFormBlock()
        html = block.render(block.to_python({
            'form': self.form.pk,
        }))
        expected_html = '\n'.join([
            '<h2>Form</h2>',
            '<form action="/forms/1/submit/" method="post" id="streamforms_1" novalidate>',
            '<div class="field-row">',
            '<label for="id_name">name</label>',
            '<input type="text" name="name" maxlength="255" required id="id_name" />',
            '</div>',
            '<input type="submit" value="Submit">',
            '</form>',
        ])
        self.assertHTMLEqual(html, expected_html)
