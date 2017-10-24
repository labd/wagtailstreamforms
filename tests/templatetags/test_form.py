from wagtailstreamforms.models import BasicForm, FormField

from ..test_case import AppTestCase


class TemplateTagTests(AppTestCase):

    def setUp(self):
        self.form = BasicForm.objects.create(
            pk=100,
            name='Form',
            slug='the-form',
            template_name='streamforms/form_block.html'
        )
        self.field = FormField.objects.create(
            form=self.form,
            label='name',
            field_type='singleline'
        )

    def test_render(self):
        fake_request = self.rf.get('/')
        html = self.render_template(
            """{% load streamforms_tags %}{% streamforms_form "the-form" "some-ref" "." %}""",
            {'request': fake_request}
        )

        expected_html = '\n'.join([
            '<h2>Form</h2>',
            '<form action="." method="post" novalidate>',
            '<input id="id_form_id" name="form_id" type="hidden" value="100">',
            '<input id="id_form_reference" name="form_reference" type="hidden" value="some-ref">',
            '<div class="field-row">',
            '<label for="id_name">name</label>',
            '<input type="text" name="name" maxlength="255" required id="id_name" />',
            '</div>',
            '<input type="submit" value="Submit">',
            '</form>',
        ])

        self.assertHTMLEqual(html, expected_html)

    def test_invalid_slug_renders_empty_content(self):
        fake_request = self.rf.get('/')
        html = self.render_template(
            """{% load streamforms_tags %}{% streamforms_form "foooo" "some-ref" "." %}""",
            {'request': fake_request}
        )

        self.assertHTMLEqual(html, '')
