import json

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.models import ClusterableModel
from wagtail.core.models import Page

from wagtailstreamforms.conf import get_setting
from wagtailstreamforms.models import BaseForm, FormField, FormSubmission
from wagtailstreamforms.models.form import get_default_form_content_type

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(BaseForm, ClusterableModel))

    def test_str(self):
        model = BaseForm(name='form')
        self.assertEqual(model.__str__(), model.name)

    def test_ordering(self):
        self.assertEqual(BaseForm._meta.ordering, ['name', ])

    def test_get_default_form_content_type(self):
        self.assertEqual(get_default_form_content_type(), ContentType.objects.get_for_model(BaseForm))


class ModelFieldTests(AppTestCase):

    def test_name(self):
        field = self.get_field(BaseForm, 'name')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_slug(self):
        field = self.get_field(BaseForm, 'slug')
        self.assertModelField(field, models.SlugField)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.allow_unicode)
        self.assertTrue(field.unique)

    def test_content_type(self):
        field = self.get_field(BaseForm, 'content_type')
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertEqual(field.remote_field.model, ContentType)
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    def test_template_name(self):
        field = self.get_field(BaseForm, 'template_name')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertEqual(field.choices, get_setting('FORM_TEMPLATES'))

    def test_submit_button_text(self):
        field = self.get_field(BaseForm, 'submit_button_text')
        self.assertModelField(field, models.CharField, False, False, 'Submit')
        self.assertEqual(field.max_length, 100)

    def test_store_submission(self):
        field = self.get_field(BaseForm, 'store_submission')
        self.assertModelField(field, models.BooleanField, False, False, False)

    def test_add_recaptcha(self):
        field = self.get_field(BaseForm, 'add_recaptcha')
        self.assertModelField(field, models.BooleanField, False, False, False)

    def test_success_message(self):
        field = self.get_field(BaseForm, 'success_message')
        self.assertModelField(field, models.CharField, False, True)
        self.assertEqual(field.max_length, 255)

    def test_error_message(self):
        field = self.get_field(BaseForm, 'error_message')
        self.assertModelField(field, models.CharField, False, True)
        self.assertEqual(field.max_length, 255)

    def test_post_redirect_page(self):
        field = self.get_field(BaseForm, 'post_redirect_page')
        self.assertModelPKField(field, Page, models.SET_NULL, True, True)


class ModelPropertyTests(AppTestCase):

    def test_form(self, store_submission=False):
        form = BaseForm.objects.create(
            name='Form', 
            template_name='streamforms/form_block.html', 
            store_submission=store_submission,
            slug='form'
        )
        FormField.objects.bulk_create([
            FormField(form=form, label='singleline', field_type='singleline'),
            FormField(form=form, label='multiline', field_type='multiline'),
            FormField(form=form, label='email', field_type='email'),
            FormField(form=form, label='number', field_type='number'),
            FormField(form=form, label='url', field_type='url'),
            FormField(form=form, label='checkbox', field_type='checkbox'),
            FormField(form=form, label='checkboxes', field_type='checkboxes', choices='A,B,C'),
            FormField(form=form, label='dropdown', field_type='dropdown', choices='A,B,C'),
            FormField(form=form, label='multiselect', field_type='multiselect', choices='A,B,C'),
            FormField(form=form, label='radio', field_type='radio', choices='A,B,C'),
            FormField(form=form, label='date', field_type='date'),
            FormField(form=form, label='datetime', field_type='datetime'),
            FormField(form=form, label='regexfield', field_type='regexfield')
        ])
        return form

    def test_clean_raises_error_when_duplicate_slug(self):
        form = self.test_form()

        new_form = BaseForm(name=form.name, slug=form.slug, template_name=form.template_name)

        with self.assertRaises(ValidationError) as cm:
            new_form.full_clean()

        self.assertEqual(
            cm.exception.message_dict,
            {'slug': ['Form with this Slug already exists.']}
        )

    def test_copy(self):
        form = self.test_form()

        copied = form.copy()

        self.assertNotEqual(copied.pk, form.pk)
        self.assertEqual(copied.specific_class, form.specific_class)

    def test_copy_has_form_fields(self):
        form = self.test_form()

        copied = form.copy()

        self.assertEqual(copied.get_form_fields().count(), 13)

    def test_copy_does_not_copy_form_submissions(self):
        # it should never do any way as its a reverse fk but incase modelcluster
        # ever changes we are testing for it

        form = self.test_form()
        FormSubmission.objects.create(form_data='{}', form=form)

        copied = form.copy()

        self.assertEqual(FormSubmission.objects.filter(form=copied).count(), 0)

    def test_get_data_fields(self):
        form = self.test_form()
        expected_fields = [
            ('submit_time', _('Submission date')),
            ('singleline', _('singleline')),
            ('multiline', _('multiline')),
            ('email', _('email')),
            ('number', _('number')),
            ('url', _('url')),
            ('checkbox', _('checkbox')),
            ('checkboxes', _('checkboxes')),
            ('dropdown', _('dropdown')),
            ('multiselect', _('multiselect')),
            ('radio', _('radio')),
            ('date', _('date')),
            ('datetime', _('datetime')),
            ('regexfield', _('regexfield'))
        ]
        self.assertEqual(form.get_data_fields(), expected_fields)

    def test_get_form(self):
        form = self.test_form()
        actual_fields = [f for f in form.get_form().fields]
        expected_fields = [
            'singleline',
            'multiline',
            'email',
            'number',
            'url',
            'checkbox',
            'checkboxes',
            'dropdown',
            'multiselect',
            'radio',
            'date',
            'datetime',
            'regexfield',
            'form_id',
            'form_reference'
        ]
        self.assertEqual(actual_fields, expected_fields)

    def test_get_form_fields(self):
        form = self.test_form()
        self.assertEqual(form.get_form_fields().count(), 13)

    def test_get_form_parameters(self):
        form = BaseForm()
        self.assertEqual(form.get_form_parameters(), {})

    def test_get_submission_class(self):
        form = self.test_form()
        self.assertEqual(form.get_submission_class(), FormSubmission)

    def test_process_form_submission__saves_record_when_store_submission_is_true(self):
        form = self.test_form(True)
        data = {
            'singleline': 'text',
            'multiline': 'text\r\ntext',
            'email': 'foo@example.com',
            'number': 1,
            'url': 'http://www.google.com',
            'checkbox': 'on',
            'checkboxes': ['A', 'B'],
            'dropdown': 'A',
            'multiselect': ['A', 'B'],
            'radio': 'A',
            'date': '2017-01-01',
            'datetime': '2017-01-01 00:00:00',
            'regexfield': 'text',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        }
        form_class = form.get_form(data)
        assert form_class.is_valid()
        form.process_form_submission(form_class)
        saved_form_data = json.dumps(form_class.cleaned_data, cls=DjangoJSONEncoder)
        self.assertEqual(form.get_submission_class().objects.count(), 1)
        self.assertEqual(form.get_submission_class().objects.all()[0].form_data, saved_form_data)
    
    def test_process_form_submission__does_not_save_record_when_store_submission_is_false(self):
        form = self.test_form()
        data = {
            'singleline': 'text',
            'multiline': 'text\r\ntext',
            'email': 'foo@example.com',
            'number': 1,
            'url': 'http://www.google.com',
            'checkbox': 'on',
            'checkboxes': ['A', 'B'],
            'dropdown': 'A',
            'multiselect': ['A', 'B'],
            'radio': 'A',
            'date': '2017-01-01',
            'datetime': '2017-01-01 00:00:00',
            'regexfield': 'text',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        }
        form_class = form.get_form(data)
        assert form_class.is_valid()
        form.process_form_submission(form_class)
        self.assertEqual(form.get_submission_class().objects.count(), 0)

    def test_specific(self):
        form = self.test_form()
        self.assertEqual(form.specific, form)

    def test_specific_class(self):
        form = self.test_form()
        self.assertEqual(form.specific_class, form.__class__)
