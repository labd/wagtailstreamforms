from django.core import mail
from django.db import models

from wagtailstreamforms.fields import MultiEmailField
from wagtailstreamforms.models import BaseForm, EmailForm, AbstractEmailForm

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(AbstractEmailForm, BaseForm))

    def test_ignored_fields(self):
        self.assertEqual(AbstractEmailForm.ignored_fields, ['recaptcha', 'form_id', 'form_reference'])

    def test_abstract(self):
        self.assertTrue(AbstractEmailForm._meta.abstract)


class ModelFieldTests(AppTestCase):

    def test_subject(self):
        field = self.get_field(AbstractEmailForm, 'subject')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_from_address(self):
        field = self.get_field(AbstractEmailForm, 'from_address')
        self.assertModelField(field, models.EmailField)

    def test_to_addresses(self):
        field = self.get_field(AbstractEmailForm, 'to_addresses')
        self.assertModelField(field, MultiEmailField)

    def test_message(self):
        field = self.get_field(AbstractEmailForm, 'message')
        self.assertModelField(field, models.TextField)

    def test_fail_silently(self):
        field = self.get_field(AbstractEmailForm, 'fail_silently')
        self.assertModelField(field, models.BooleanField, False, False, False)


class ModelPropertyTests(AppTestCase):
    fixtures = ['test.json']

    # testing the usage via EmailForm as it inherits this class

    def test_form(self):
        form = EmailForm.objects.get(pk=2)
        return form

    def test_inheritance(self):
        self.assertTrue(issubclass(EmailForm, AbstractEmailForm))

    def test_copy_is_right_class(self):
        form = self.test_form()

        copied = BaseForm.objects.get(pk=form.pk).copy()

        self.assertNotEqual(copied.pk, form.pk)
        self.assertEqual(copied.specific_class, EmailForm)

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
        self.assertEqual(form.get_submission_class().objects.count(), 1)

    def test_specific_from_baseform_is_correct_object(self):
        form = self.test_form()
        self.assertEqual(form.specific, form)
        self.assertEqual(BaseForm.objects.get(pk=form.pk).specific, form)

    def test_specific_class_from_baseform_is_correct_class(self):
        form = self.test_form()
        self.assertEqual(form.specific_class, form.__class__)
        self.assertEqual(BaseForm.objects.get(pk=form.pk).specific_class, form.__class__)
