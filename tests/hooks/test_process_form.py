from django.contrib.auth.models import AnonymousUser
from django.test import override_settings
from django.test.client import Client
from mock import patch
from wagtail.core.models import Page

from wagtailstreamforms.models import BasicForm, FormField
from wagtailstreamforms.wagtail_hooks import process_form
from ..test_case import AppTestCase


class TestHook(AppTestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.page = Page.objects.get(url_path='/home/')
        self.mock_messages_error = patch('django.contrib.messages.error')
        self.mock_messages_success = patch('django.contrib.messages.success')
        self.mock_error_message = self.mock_messages_error.start()
        self.mock_success_message = self.mock_messages_success.start()

    def test_form(self):
        form = BasicForm.objects.get(pk=1)
        return form

    def test_get_returns_nothing(self):
        fake_request = self.rf.get('/fake/')
        fake_request.user = AnonymousUser()

        response = process_form(self.page, fake_request)

        self.assertIsNone(response)

    @override_settings(WAGTAILSTREAMFORMS_ENABLE_FORM_PROCESSING=False)
    def test_hook_disabled_when_setting_false(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {
            'name': 'Bill',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        response = process_form(self.page, fake_request)

        self.assertIsNone(response)

    def test_valid_post_redirects__to_the_forms_post_redirect_page(self):
        redirect_to = self.page.add_child(instance=Page(title="another", slug="another"))
        form = self.test_form()
        form.post_redirect_page = redirect_to
        form.save()
        fake_request = self.rf.post('/fake/', {
            'name': 'Bill',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        response = process_form(self.page, fake_request)
        response.client = Client()

        self.assertRedirects(response, redirect_to.get_url(fake_request))

    def test_valid_post_redirects__falls_back_to_current_page(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {
            'name': 'Bill',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        response = process_form(self.page, fake_request)
        response.client = Client()

        self.assertRedirects(response, self.page.get_url(fake_request))

    def test_valid_post_saves_submission(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {
            'name': 'Bill',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        process_form(self.page, fake_request)

        self.assertEqual(form.get_submission_class().objects.count(), 1)

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
        form.success_message = ''
        form.save()
        fake_request = self.rf.post('/fake/', {
            'name': 'Bill',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        process_form(self.page, fake_request)

        assert not self.mock_success_message.called, 'messages.success should not have been called'

    def test_error_message__sent_when_form_has_message(self):
        form = self.test_form()
        form.error_message = 'oops'
        form.save()
        fake_request = self.rf.post('/fake/', {
            'name': '',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        process_form(self.page, fake_request)

        self.assertEqual(self.mock_error_message.call_args[0][1], 'oops')
        self.assertEqual(self.mock_error_message.call_args[1], {'fail_silently': True})

    def test_error_message__not_sent_when_form_has_no_message(self):
        form = self.test_form()
        form.error_message = ''
        form.save()
        fake_request = self.rf.post('/fake/', {
            'name': '',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        process_form(self.page, fake_request)

        assert not self.mock_error_message.called, 'messages.error should not have been called'

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

    def test_invalid_form_returns_response_with_form(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {
            'name': '',
            'form_id': form.pk,
            'form_reference': 'some-ref'
        })
        fake_request.user = AnonymousUser()

        response = process_form(self.page, fake_request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['invalid_stream_form_reference'], 'some-ref')

        invalid_form = response.context_data['invalid_stream_form']
        self.assertEqual(invalid_form.errors, {'name': ['This field is required.']})

    def tearDown(self):
        self.mock_messages_error.stop()
        self.mock_messages_success.stop()
