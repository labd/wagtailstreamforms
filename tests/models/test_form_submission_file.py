from django.db import models

from wagtailstreamforms.models import FormSubmission, FormSubmissionFile

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_str(self):
        model = FormSubmissionFile(file=self.get_file())
        self.assertEqual(model.__str__(), model.file.name)

    def test_ordering(self):
        self.assertEqual(FormSubmissionFile._meta.ordering, ['field', 'file'])


class ModelFieldTests(AppTestCase):

    def test_submission(self):
        field = self.get_field(FormSubmissionFile, 'submission')
        self.assertModelPKField(field, FormSubmission, models.CASCADE)

    def test_field(self):
        field = self.get_field(FormSubmissionFile, 'field')
        self.assertModelField(field, models.CharField)

    def test_file(self):
        field = self.get_field(FormSubmissionFile, 'file')
        self.assertModelField(field, models.FileField)


class ModelPropertyTests(AppTestCase):

    def test_url(self):
        model = FormSubmissionFile(file=self.get_file())
        self.assertEqual(model.url, model.file.url)
