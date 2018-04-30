from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.models import ClusterableModel

from wagtail.core.models import Page

from wagtailstreamforms.conf import get_setting
from wagtailstreamforms.fields import HookSelectField
from wagtailstreamforms.models import Form, FormField, FormSubmission

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(Form, ClusterableModel))

    def test_str(self):
        model = Form(name='form')
        self.assertEqual(model.__str__(), model.name)

    def test_ordering(self):
        self.assertEqual(Form._meta.ordering, ['name', ])


class ModelFieldTests(AppTestCase):

    def test_name(self):
        field = self.get_field(Form, 'name')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_slug(self):
        field = self.get_field(Form, 'slug')
        self.assertModelField(field, models.SlugField)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.allow_unicode)
        self.assertTrue(field.unique)

    def test_template_name(self):
        field = self.get_field(Form, 'template_name')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)
        self.assertEqual(field.choices, get_setting('FORM_TEMPLATES'))

    def test_submit_button_text(self):
        field = self.get_field(Form, 'submit_button_text')
        self.assertModelField(field, models.CharField, False, False, 'Submit')
        self.assertEqual(field.max_length, 100)

    def test_success_message(self):
        field = self.get_field(Form, 'success_message')
        self.assertModelField(field, models.CharField, False, True)
        self.assertEqual(field.max_length, 255)

    def test_error_message(self):
        field = self.get_field(Form, 'error_message')
        self.assertModelField(field, models.CharField, False, True)
        self.assertEqual(field.max_length, 255)

    def test_post_redirect_page(self):
        field = self.get_field(Form, 'post_redirect_page')
        self.assertModelPKField(field, Page, models.SET_NULL, True, True)

    def test_process_form_submission_hooks(self):
        field = self.get_field(Form, 'process_form_submission_hooks')
        self.assertModelField(field, HookSelectField, False, True)


class ModelPropertyTests(AppTestCase):

    def test_form(self):
        form = Form.objects.create(
            name='Form', 
            template_name='streamforms/form_block.html',
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
            FormField(form=form, label='datetime', field_type='datetime')
        ])
        return form

    def test_clean_raises_error_when_duplicate_slug(self):
        form = self.test_form()

        new_form = Form(name=form.name, slug=form.slug, template_name=form.template_name)

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
        self.assertEqual(copied.__class__, form.__class__)

    def test_copy_has_form_fields(self):
        form = self.test_form()

        copied = form.copy()

        self.assertEqual(copied.get_form_fields().count(), 12)

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
            ('datetime', _('datetime'))
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
            'form_id',
            'form_reference'
        ]
        self.assertEqual(actual_fields, expected_fields)

    def test_get_form_fields(self):
        form = self.test_form()
        self.assertEqual(form.get_form_fields().count(), 12)

    def test_get_form_parameters(self):
        form = Form()
        self.assertEqual(form.get_form_parameters(), {})

    def test_get_submission_class(self):
        form = self.test_form()
        self.assertEqual(form.get_submission_class(), FormSubmission)

    def test_process_form_submission(self):
        def complete_hook(instance, form):
            instance._completed = True

        with self.register_hook('process_form_submission', complete_hook, order=-1):
            instance = self.test_form()
            form_class = instance.get_form_class()

            # wont call registered hooks that are not saved
            instance.process_form_submission(form_class)
            self.assertFalse(hasattr(instance, '_completed'))

            # selected hooks
            instance.process_form_submission_hooks = ['complete_hook']
            instance.save()

            instance.process_form_submission(form_class)
            self.assertTrue(instance._completed)
