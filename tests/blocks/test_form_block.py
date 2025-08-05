from wagtailstreamforms.blocks import WagtailFormBlock
from wagtailstreamforms.models import Form

from ..test_case import AppTestCase


class TestFormBlockTestCase(AppTestCase):
    fixtures = ["test.json"]

    def setUp(self):
        self.form = Form.objects.get(pk=1)

    def test_render(self):
        block = WagtailFormBlock()

        html = block.render(
            block.to_python(
                {"form": self.form.pk, "form_action": ".", "form_reference": "some-ref"}
            )
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
        self.assertIn('<input type="url"', html)
        self.assertIn('<input type="number"', html)
        self.assertIn("<select", html)
        self.assertIn('<input type="radio"', html)
        self.assertIn('<input type="checkbox"', html)
        self.assertIn('<input type="file"', html)

        # Check field labels
        self.assertIn('<label for="id_singleline">singleline</label>', html)
        self.assertIn('<label for="id_multiline">multiline</label>', html)

        # Check help text
        self.assertIn('<p class="help-text">Help</p>', html)

        # Check dropdown options
        self.assertIn('<option value="Option 1">Option 1</option>', html)
        self.assertIn('<option value="Option 2">Option 2</option>', html)
        self.assertIn('<option value="Option 3">Option 3</option>', html)

        # Check submit button
        self.assertIn('<input type="submit" value="Submit">', html)

    def test_render_when_form_deleted(self):
        block = WagtailFormBlock()

        html = block.render(
            block.to_python({"form": 100, "form_action": "/foo/", "form_reference": "some-ref"})
        )

        self.assertIn("<p>Sorry, this form has been deleted.</p>", html)

    def test_clean_adds_form_reference(self):
        block = WagtailFormBlock()

        value = block.clean({"form": self.form.pk, "form_action": "/foo/"})

        self.assertIsNotNone(value.get("form_reference"))

    def test_clean_keeps_existing_form_reference(self):
        block = WagtailFormBlock()

        value = block.clean(
            {"form": self.form.pk, "form_action": "/foo/", "form_reference": "some-ref"}
        )

        self.assertEqual(value.get("form_reference"), "some-ref")

    def test_context_has_form(self):
        block = WagtailFormBlock()

        context = block.get_context(
            block.to_python(
                {
                    "form": self.form.pk,
                    "form_action": "/foo/",
                    "form_reference": "some-ref",
                }
            )
        )

        self.assertIsNotNone(context["form"])

    def test_context_form_is_invalid_when_parent_context_has_this_form_with_errors(
        self,
    ):
        invalid_form = self.form.get_form({"form_id": self.form.id, "form_reference": "some-ref"})
        assert not invalid_form.is_valid()

        self.assertDictEqual(
            invalid_form.errors,
            {
                "singleline": ["This field is required."],
                "multiline": ["This field is required."],
                "date": ["This field is required."],
                "datetime": ["This field is required."],
                "email": ["This field is required."],
                "url": ["This field is required."],
                "number": ["This field is required."],
                "dropdown": ["This field is required."],
                "radio": ["This field is required."],
                "checkboxes": ["This field is required."],
                "checkbox": ["This field is required."],
                "hidden": ["This field is required."],
                "singlefile": ["This field is required."],
                "multifile": ["This field is required."],
            },
        )

        # this is the context a page will set for an invalid form
        parent_context = {
            "invalid_stream_form_reference": "some-ref",
            "invalid_stream_form": invalid_form,
        }

        block = WagtailFormBlock()

        # get a new block context
        context = block.get_context(
            block.to_python(
                {
                    "form": self.form.pk,
                    "form_action": "/foo/",
                    "form_reference": "some-ref",
                }
            ),
            parent_context,
        )

        # finally make sure the form in the block is the one with errors
        self.assertEqual(context["form"], invalid_form)
