from django.db import models

from multi_email_field.fields import MultiEmailField
from wagtail_streamforms.models.partials import EmailPartial

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(EmailPartial, models.Model))

    def test_abstract(self):
        self.assertTrue(EmailPartial._meta.abstract)


class ModelFieldTests(AppTestCase):

    def test_subject(self):
        field = self.get_field(EmailPartial, 'subject')
        self.assertModelField(field, models.CharField)
        self.assertEquals(field.max_length, 255)

    def test_from_address(self):
        field = self.get_field(EmailPartial, 'from_address')
        self.assertModelField(field, models.EmailField)

    def test_to_addresses(self):
        field = self.get_field(EmailPartial, 'to_addresses')
        self.assertModelField(field, MultiEmailField)

    def test_message(self):
        field = self.get_field(EmailPartial, 'message')
        self.assertModelField(field, models.TextField)

    def test_fail_silently(self):
        field = self.get_field(EmailPartial, 'fail_silently')
        self.assertModelField(field, models.BooleanField, False, False, False)
