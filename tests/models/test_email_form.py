from django.core import mail

from wagtail_streamforms.models import BaseForm, EmailForm, FormField
from wagtail_streamforms.models.partials import EmailPartial

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(EmailForm, BaseForm))
        self.assertTrue(issubclass(EmailForm, EmailPartial))


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
        form_class = form.get_form({'name': 'foo'})
        assert form_class.is_valid()
        form.process_form_submission(form_class)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, form.subject)

    def test_process_form_submission__still_saves_submission(self):
        form = self.test_form(True)
        form_class = form.get_form({'name': 'foo'})
        assert form_class.is_valid()
        form.process_form_submission(form_class)
        self.assertEquals(form.formsubmission_set.count(), 1)