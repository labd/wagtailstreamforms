import mock

from django import forms

from captcha.fields import ReCaptchaField
from wagtailstreamforms.forms import FormBuilder
from wagtailstreamforms.models import BaseForm, FormField, RegexFieldValidator

from ..test_case import AppTestCase


class FormBuilderTests(AppTestCase):

    def setUp(self):
        self.form = BaseForm.objects.create(
            name='Form',
            slug='form',
            template_name='streamforms/form_block.html',
        )
        self.field = FormField.objects.create(
            form=self.form,
            label='My regex',
            field_type='regexfield'
        )

    # regex field

    def test_regex_field_exists(self):
        fb = FormBuilder(self.form.get_form_fields(), add_recaptcha=False)
        form_class = fb.get_form_class()
        field_names = form_class.base_fields.keys()
        self.assertIn('my-regex', field_names)
        self.assertIsInstance(form_class.base_fields['my-regex'], forms.RegexField)

    def test_regex_field_default_options(self):
        fb = FormBuilder(self.form.get_form_fields(), add_recaptcha=False)
        form_class = fb.get_form_class()
        self.assertEquals(form_class.base_fields['my-regex'].regex.pattern, '(.*?)')

    def test_regex_field_with_validator_has_correct_options_set(self):
        validator = RegexFieldValidator.objects.create(
            name='Positive Number',
            regex='/^\d+$/',
            error_message='Please enter a positive number.'
        )
        self.field.regex_validator = validator
        self.field.save()
        fb = FormBuilder(self.form.get_form_fields(), add_recaptcha=False)
        form_class = fb.get_form_class()
        self.assertEquals(form_class.base_fields['my-regex'].regex.pattern, validator.regex)
        self.assertEquals(form_class.base_fields['my-regex'].error_messages['invalid'], validator.error_message)

    # recaptcha field

    @mock.patch('wagtailstreamforms.forms.recaptcha_enabled')
    def test_recaptcha_field_not_added_when_not_enabled(self, mock_stub):
        mock_stub.return_value = False
        fb = FormBuilder(self.form.get_form_fields(), add_recaptcha=False)
        form_class = fb.get_form_class()
        field_names = form_class.base_fields.keys()
        self.assertNotIn('recaptcha', field_names)

    @mock.patch('wagtailstreamforms.forms.recaptcha_enabled')
    def test_recaptcha_field_added(self, mock_stub):
        mock_stub.return_value = True
        fb = FormBuilder(self.form.get_form_fields(), add_recaptcha=True)
        form_class = fb.get_form_class()
        field_names = form_class.base_fields.keys()
        self.assertIn('recaptcha', field_names)
        self.assertIsInstance(form_class.base_fields['recaptcha'], ReCaptchaField)
