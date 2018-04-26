from django.db import models

from wagtailstreamforms.models import Form, FormSubmission

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_str(self):
        model = FormSubmission(form_data='{"foo": 1}')
        self.assertEqual(model.__str__(), model.form_data)

    def test_ordering(self):
        self.assertEqual(FormSubmission._meta.ordering, ['-submit_time', ])


class ModelFieldTests(AppTestCase):

    def test_form_data(self):
        field = self.get_field(FormSubmission, 'form_data')
        self.assertModelField(field, models.TextField)

    def test_form(self):
        field = self.get_field(FormSubmission, 'form')
        self.assertModelPKField(field, Form, models.CASCADE)

    def test_submit_time(self):
        field = self.get_field(FormSubmission, 'submit_time')
        self.assertModelField(field, models.DateTimeField, False, True)
        self.assertTrue(field.auto_now_add)


class ModelPropertyTests(AppTestCase):
    fixtures = ['test.json']

    def test_get_data(self):
        form = Form.objects.get(pk=1)
        model = FormSubmission.objects.create(form_data='{"foo": 1}', form=form)
        expected_data = {"foo": 1, "submit_time": model.submit_time}
        self.assertEqual(model.get_data(), expected_data)

    def test_get_data_blank(self):
        form = Form.objects.get(pk=1)
        model = FormSubmission.objects.create(form_data='{}', form=form)
        expected_data = {"submit_time": model.submit_time}
        self.assertEqual(model.get_data(), expected_data)
