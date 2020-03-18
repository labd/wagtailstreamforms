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
            '<form action="." enctype="multipart/form-data" method="post" novalidate>',
            '<input type="hidden" name="hidden" id="id_hidden" />',
            '<input id="id_form_id" name="form_id" type="hidden" value="%s">' % self.form.pk,
            '<input id="id_form_reference" name="form_reference" type="hidden" value="some-ref">',
            '<div class="field-row">'
            '<label for="id_singleline">singleline</label>'
            '<input type="text" name="singleline" required id="id_singleline" />'
            '<p class="help-text">Help</p>'
            '</div>',
            '<div class="field-row">'
            '<label for="id_multiline">multiline</label>'
            '<textarea name="multiline" cols="40" rows="10" required id="id_multiline">'
            '</textarea>'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label for="id_date">date</label>'
            '<input type="text" name="date" value="" required id="id_date" />'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label for="id_datetime">datetime</label>'
            '<input type="text" name="datetime" value="" required id="id_datetime" />'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label for="id_email">email</label>'
            '<input type="email" name="email" required id="id_email" />'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label for="id_url">url</label>'
            '<input type="url" name="url" required id="id_url" />'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label for="id_number">number</label>'
            '<input type="number" name="number" step="any" required id="id_number" />'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label for="id_dropdown">dropdown</label>'
            '<select name="dropdown" id="id_dropdown">'
            '<option value="Option 1">Option 1</option>'
            '<option value="Option 2">Option 2</option>'
            '<option value="Option 3">Option 3</option></select>'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label for="id_multiselect">multiselect</label>'
            '<select name="multiselect" required id="id_multiselect" multiple="multiple">'
            '<option value="Option 1">Option 1</option>'
            '<option value="Option 2">Option 2</option>'
            '<option value="Option 3">Option 3</option></select>'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label for="id_radio_0">radio</label>'
            '<ul id="id_radio">'
            '<li><label for="id_radio_0">'
            '<input type="radio" name="radio" value="Option 1" required id="id_radio_0" /> Option 1'
            '</label></li>'
            '<li><label for="id_radio_1">'
            '<input type="radio" name="radio" value="Option 2" required id="id_radio_1" /> Option 2'
            '</label></li>'
            '<li><label for="id_radio_2">'
            '<input type="radio" name="radio" value="Option 3" required id="id_radio_2" /> Option 3'
            '</label></li></ul>'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label>checkboxes</label>'
            '<ul id="id_checkboxes">'
            '<li><label for="id_checkboxes_0">'
            '<input type="checkbox" name="checkboxes" value="Option 1" id="id_checkboxes_0" /> Option 1'
            '</label></li>'
            '<li><label for="id_checkboxes_1">'
            '<input type="checkbox" name="checkboxes" value="Option 2" id="id_checkboxes_1" /> Option 2'
            '</label></li>'
            '<li><label for="id_checkboxes_2">'
            '<input type="checkbox" name="checkboxes" value="Option 3" id="id_checkboxes_2" /> Option 3'
            '</label></li></ul>'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label for="id_checkbox">checkbox</label>'
            '<input type="checkbox" name="checkbox" required id="id_checkbox" />'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label for="id_singlefile">singlefile</label>'
            '<input type="file" name="singlefile" required id="id_singlefile" />'
            '<p class="help-text">Help</p>'
            '</div>'
            '<div class="field-row">'
            '<label for="id_multifile">multifile</label>'
            '<input type="file" name="multifile" multiple required id="id_multifile" />'
            '<p class="help-text">Help</p>'
            '</div>'
            '<input type="submit" value="Submit">'
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
