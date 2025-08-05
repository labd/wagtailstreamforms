from wagtailstreamforms.models import Form

from ..test_case import AppTestCase


class TemplateTagTests(AppTestCase):
    fixtures = ["test.json"]

    def setUp(self):
        self.form = Form.objects.get(pk=1)

    def test_render(self):
        fake_request = self.rf.get("/")
        html = self.render_template(
            """{% load streamforms_tags %}{% streamforms_form "basic-form" "some-ref" "." %}""",
            {"request": fake_request},
        )

        # Test critical elements that should be present
        self.assertIn("<h2>Basic Form</h2>", html)
        self.assertIn('action="."', html)
        self.assertIn('method="post"', html)
        self.assertIn('enctype="multipart/form-data"', html)

        # Check hidden fields
        self.assertIn(f'<input type="hidden" name="form_id" value="{self.form.pk}"', html)
        self.assertIn('<input type="hidden" name="form_reference" value="some-ref"', html)

        # Check form field types
        self.assertIn('<input type="text"', html)
        self.assertIn("<textarea", html)
        self.assertIn('<input type="email"', html)
        self.assertIn("<select", html)
        self.assertIn('<input type="radio"', html)
        self.assertIn('<input type="checkbox"', html)
        self.assertIn('<input type="file"', html)

        # Check submit button
        self.assertIn('<input type="submit" value="Submit">', html)

    def test_invalid_slug_renders_empty_content(self):
        fake_request = self.rf.get("/")
        html = self.render_template(
            """{% load streamforms_tags %}{% streamforms_form "non-existing-slug" "some-ref" "." %}""",
            {"request": fake_request},
        )

        self.assertHTMLEqual(html, "")
