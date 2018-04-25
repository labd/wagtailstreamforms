from wagtailstreamforms.models import Form

from ..test_case import AppTestCase


class TemplateTagTests(AppTestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.form = Form.objects.get(pk=1)

    def test_render(self):
        fake_request = self.rf.get('/')
        html = self.render_template(
            """{% load streamforms_tags %}{% streamforms_form "basic-form" "some-ref" "." %}""",
            {'request': fake_request}
        )

        expected_html = '\n'.join([
            '<h2>Basic Form</h2>',
            '<form action="." method="post" novalidate>',
            '<input id="id_form_id" name="form_id" type="hidden" value="%s">' % self.form.pk,
            '<input id="id_form_reference" name="form_reference" type="hidden" value="some-ref">',
            '<div class="field-row">',
            '<label for="id_name">Name</label>',
            '<input type="text" name="name" maxlength="255" required id="id_name" />',
            '<p class="help-text">Please enter your name</p>',
            '</div>',
            '<input type="submit" value="Submit">',
            '</form>',
        ])

        self.assertHTMLEqual(html, expected_html)

    def test_invalid_slug_renders_empty_content(self):
        fake_request = self.rf.get('/')
        html = self.render_template(
            """{% load streamforms_tags %}{% streamforms_form "non-existing-slug" "some-ref" "." %}""",
            {'request': fake_request}
        )

        self.assertHTMLEqual(html, '')
