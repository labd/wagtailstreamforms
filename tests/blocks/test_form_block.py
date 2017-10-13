from wagtailstreamforms.blocks import WagtailFormBlock
from wagtailstreamforms.models import BasicForm, FormField

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
            'form_action': '/foo/'
        }))

        expected_html = '\n'.join([
            '<h2>Form</h2>',
            '<form action="/foo/" method="post" novalidate>',
            '<input name="form_id" type="hidden" value="%s">' % self.form.pk,
            '<div class="field-row">',
            '<label for="id_name">name</label>',
            '<input type="text" name="name" maxlength="255" required id="id_name" />',
            '</div>',
            '<input type="submit" value="Submit">',
            '</form>',
        ])

        self.assertHTMLEqual(html, expected_html)

    def test_context_has_form(self):
        block = WagtailFormBlock()

        context = block.get_context(block.to_python({
            'form': self.form.pk,
            'form_action': '/foo/'
        }))

        self.assertIsNotNone(context['form'])

    def test_context_form_is_invalid_when_parent_context_has_this_form_with_errors(self):
        invalid_form = self.form.get_form({'form_id': self.form.id})
        assert not invalid_form.is_valid()

        self.assertEquals(invalid_form.errors, {'name': ['This field is required.']})

        # this is the context a page will set for an invalid form
        parent_context = {
            'invalid_stream_form_id': self.form.id,
            'invalid_stream_form': invalid_form
        }

        block = WagtailFormBlock()

        # get a new block context
        context = block.get_context(block.to_python({
            'form': self.form.pk,
            'form_action': '/foo/'
        }), parent_context)

        # finally make sure the form in the block is the one with errors
        self.assertEquals(context['form'], invalid_form)
