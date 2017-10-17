from django.core import mail
from django.db import models

from multi_email_field.fields import MultiEmailField
from wagtailstreamforms.models import BaseForm, EmailForm, FormField

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(EmailForm, BaseForm))


class ModelFieldTests(AppTestCase):

    def test_subject(self):
        field = self.get_field(EmailForm, 'subject')
        self.assertModelField(field, models.CharField)
        self.assertEquals(field.max_length, 255)

    def test_from_address(self):
        field = self.get_field(EmailForm, 'from_address')
        self.assertModelField(field, models.EmailField)

    def test_to_addresses(self):
        field = self.get_field(EmailForm, 'to_addresses')
        self.assertModelField(field, MultiEmailField)

    def test_message(self):
        field = self.get_field(EmailForm, 'message')
        self.assertModelField(field, models.TextField)

    def test_fail_silently(self):
        field = self.get_field(EmailForm, 'fail_silently')
        self.assertModelField(field, models.BooleanField, False, False, False)


class ModelPropertyTests(AppTestCase):

    def test_form(self, store_submission=False):
        form = EmailForm.objects.create(
            name='Form',
            template_name='streamforms/form_block.html',
            store_submission=store_submission,
            subject='Form Submission',
            from_address='foo@example.com',
            to_addresses=['foo@example.com', 'bar@example.com'],
            message='See data below:'
        )
        FormField.objects.create(
            form=form,
            label='name',
            field_type='singleline'
        )
        return form

    def test_process_form_submission__sends_an_email(self):
        form = self.test_form()
        form_class = form.get_form({'name': 'foo', 'form_id': form.pk})
        assert form_class.is_valid()
        form.process_form_submission(form_class)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, form.subject)

    def test_process_form_submission__still_saves_submission(self):
        form = self.test_form(True)
        form_class = form.get_form({'name': 'foo', 'form_id': form.pk})
        assert form_class.is_valid()
        form.process_form_submission(form_class)
        self.assertEquals(form.get_submission_class().objects.count(), 1)
