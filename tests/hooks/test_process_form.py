from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory
from mock import patch
from wagtail.wagtailcore.models import Page

from wagtailstreamforms.models import BasicForm, FormField
from wagtailstreamforms.wagtail_hooks import process_form
from ..test_case import AppTestCase


class TestHook(AppTestCase):

    def setUp(self):
        self.page = Page.objects.create(
            title='My Page',
            path='0002',
            depth=1
        )
        self.mock_messages_success = patch('django.contrib.messages.success')
        self.mock_success_message = self.mock_messages_success.start()

    @property
    def rf(self):
        return RequestFactory()

    def test_form(self, store_submission=False):
        form = BasicForm.objects.create(
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

    def test_get_returns_nothing(self):
        fake_request = self.rf.get('/fake/')
        fake_request.user = AnonymousUser()

        response = process_form(self.page, fake_request)

        self.assertIsNone(response)

    def test_valid_post_returns_nothing(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {
            'name': 'Bill',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        response = process_form(self.page, fake_request)

        self.assertIsNone(response)

    def test_valid_post_saves_submission(self):
        form = self.test_form(True)
        fake_request = self.rf.post('/fake/', {
            'name': 'Bill',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        process_form(self.page, fake_request)

        self.assertEquals(form.get_submission_class().objects.count(), 1)

    def test_success_message__sent_when_form_has_message(self):
        form = self.test_form()
        form.success_message = 'well done'
        form.save()
        fake_request = self.rf.post('/fake/', {
            'name': 'Bill',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        process_form(self.page, fake_request)

        self.assertEqual(self.mock_success_message.call_args[0][1], 'well done')
        self.assertEqual(self.mock_success_message.call_args[1], {'fail_silently': True})

    def test_success_message__not_sent_when_form_has_no_message(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {
            'name': 'Bill',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        process_form(self.page, fake_request)

        assert not self.mock_success_message.called, 'messages.success should not have been called'

    def test_invalid_form_id_returns_nothing(self):
        self.test_form()
        fake_request = self.rf.post('/fake/', {'form_id': 100})
        fake_request.user = AnonymousUser()

        response = process_form(self.page, fake_request)

        self.assertIsNone(response)

    def test_no_form_id_returns_nothing(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {})
        fake_request.user = AnonymousUser()

        response = process_form(self.page, fake_request)

        self.assertIsNone(response)

    def test_invalid_form_returns_correct_response(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {
            'name': '',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        response = process_form(self.page, fake_request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context_data['invalid_stream_form_reference'], 'some-ref')

        invalid_form = response.context_data['invalid_stream_form']
        self.assertEquals(invalid_form.errors, {'name': ['This field is required.']})

    def tearDown(self):
        self.mock_messages_success.stop()
