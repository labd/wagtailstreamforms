import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager
from modelcluster.models import ClusterableModel

from wagtail_streamforms.models import BaseForm, FormField

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(BaseForm, ClusterableModel))

    def test_manager(self):
        self.assertTrue(isinstance(BaseForm._default_manager, InheritanceManager))

    def test_str(self):
        model = BaseForm(name='form')
        self.assertEquals(model.__str__(), model.name)

    def test_ordering(self):
        self.assertEqual(BaseForm._meta.ordering, ['name', ])

class ModelFieldTests(AppTestCase):

    def test_name(self):
        field = self.get_field(BaseForm, 'name')
        self.assertModelField(field, models.CharField)
        self.assertEquals(field.max_length, 255)

    def test_template_name(self):
        field = self.get_field(BaseForm, 'template_name')
        self.assertModelField(field, models.CharField)
        self.assertEquals(field.max_length, 255)
        self.assertEquals(field.choices, settings.WAGTAIL_STREAMFORMS_FORM_TEMPLATES)

    def test_submit_button_text(self):
        field = self.get_field(BaseForm, 'submit_button_text')
        self.assertModelField(field, models.CharField, False, False, 'Submit')
        self.assertEquals(field.max_length, 100)

    def test_store_submission(self):
        field = self.get_field(BaseForm, 'store_submission')
        self.assertModelField(field, models.BooleanField, False, False, False)

    def test_add_recaptcha(self):
        field = self.get_field(BaseForm, 'add_recaptcha')
        self.assertModelField(field, models.BooleanField, False, False, False)

    def test_success_message(self):
        field = self.get_field(BaseForm, 'success_message')
        self.assertModelField(field, models.CharField, False, True)
        self.assertEquals(field.max_length, 255)


class ModelPropertyTests(AppTestCase):

    def test_form(self, store_submission=False):
        form = BaseForm.objects.create(
            name='Form', 
            template_name='streamforms/form_block.html', 
            store_submission=store_submission
        )
        FormField.objects.create(
            form=form, 
            label='name',
            field_type='singleline'
        )
        return form

    def test_get_form_fields(self):
        form = self.test_form()
        self.assertEquals(form.get_form_fields().count(), 1)
        self.assertEquals(form.get_form_fields()[0], form.form_fields.all()[0])

    def test_get_data_fields(self):
        form = self.test_form()
        expected_fields = [
            ('submit_time', _('Submission date')),
            ('name', _('name'))
        ]
        self.assertEquals(form.get_data_fields(), expected_fields)

    def test_get_form_parameters(self):
        form = BaseForm()
        self.assertEquals(form.get_form_parameters(), {})

    def test_get_form(self):
        form = self.test_form()
        actual_fields = [f for f in form.get_form().fields]
        expected_fields = ['name']
        self.assertEqual(actual_fields, expected_fields)
    
    def test_process_form_submission__saves_record_when_store_submission_is_true(self):
        form = self.test_form(True)
        form_class = form.get_form({'name': 'foo'})
        assert form_class.is_valid()
        form.process_form_submission(form_class)
        saved_form_data = json.dumps(form_class.cleaned_data, cls=DjangoJSONEncoder)
        self.assertEquals(form.formsubmission_set.count(), 1)
        self.assertEquals(form.formsubmission_set.all()[0].form_data, saved_form_data)
    
    def test_process_form_submission__does_not_save_record_when_store_submission_is_false(self):
        form = self.test_form()
        form_class = form.get_form({'name': 'foo'})
        assert form_class.is_valid()
        form.process_form_submission(form_class)
        self.assertEquals(form.formsubmission_set.count(), 0)
