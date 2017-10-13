from django.db import models

from wagtailstreamforms.models import BaseForm, FormSubmission

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(FormSubmission, models.Model))

    def test_str(self):
        model = FormSubmission(form_data='{"foo": 1}')
        self.assertEquals(model.__str__(), model.form_data)

    def test_ordering(self):
        self.assertEqual(FormSubmission._meta.ordering, ['-submit_time', ])


class ModelFieldTests(AppTestCase):

    def test_form_data(self):
        field = self.get_field(FormSubmission, 'form_data')
        self.assertModelField(field, models.TextField)

    def test_form(self):
        field = self.get_field(FormSubmission, 'form')
        self.assertModelPKField(field, BaseForm, models.CASCADE)

    def test_submit_time(self):
        field = self.get_field(FormSubmission, 'submit_time')
        self.assertModelField(field, models.DateTimeField, False, True)
        self.assertTrue(field.auto_now_add)


class ModelPropertyTests(AppTestCase):

    def test_get_data(self):
        form = BaseForm.objects.create(
            name='Form',
            template_name='streamforms/form_block.html'
        )
        model = FormSubmission.objects.create(form_data='{"foo": 1}', form=form)
        expected_data = {"foo": 1, "submit_time": model.submit_time}
        self.assertEquals(model.get_data(), expected_data)

    def test_get_data_blank_edge_case(self):
        form = BaseForm.objects.create(
            name='Form',
            template_name='streamforms/form_block.html'
        )
        model = FormSubmission.objects.create(form_data='', form=form)
        expected_data = {"submit_time": model.submit_time}
        self.assertEquals(model.get_data(), expected_data)
