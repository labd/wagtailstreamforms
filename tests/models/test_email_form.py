from django.core import mail
from django.db import models

from wagtailstreamforms.fields import MultiEmailField
from wagtailstreamforms.models import BaseForm, EmailForm

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(EmailForm, BaseForm))

    def test_ignored_fields(self):
        self.assertEquals(EmailForm.ignored_fields, ['recaptcha', 'form_id', 'form_reference'])


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
    fixtures = ['test.json']

    def test_form(self):
        form = EmailForm.objects.get(pk=2)
        return form

    def test_copy_is_right_class(self):
        form = self.test_form()

        copied = BaseForm.objects.get(pk=form.pk).copy()

        self.assertNotEquals(copied.pk, form.pk)
        self.assertEquals(copied.specific_class, form.specific_class)

    def test_process_form_submission__sends_an_email(self):
        form = self.test_form()
        form_class = form.get_form({
            'name': 'foo',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        assert form_class.is_valid()
        form.process_form_submission(form_class)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, form.subject)

    def test_process_form_submission__still_saves_submission(self):
        form = self.test_form()
        form_class = form.get_form({
            'name': 'foo',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        assert form_class.is_valid()
        form.process_form_submission(form_class)
        self.assertEquals(form.get_submission_class().objects.count(), 1)

    def test_specific(self):
        form = self.test_form()
        self.assertEquals(form.specific, form)
        self.assertEquals(BaseForm.objects.get(pk=form.pk).specific, form)

    def test_specific_class(self):
        form = self.test_form()
        self.assertEquals(form.specific_class, form.__class__)
        self.assertEquals(BaseForm.objects.get(pk=form.pk).specific_class, form.__class__)
