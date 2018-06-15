from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from wagtailstreamforms.wagtail_hooks import FormURLHelper

from wagtailstreamforms.models import Form

from ..test_case import AppTestCase


@override_settings(WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL='tests.ValidFormSettingsModel')
class AdvancedSettingsViewTestCase(AppTestCase):
    fixtures = ['test.json']

    def setUp(self):
        User.objects.create_superuser('user', 'user@test.com', 'password')
        self.form = Form.objects.get(pk=1)
        self.advanced_url = reverse('wagtailstreamforms:streamforms_advanced', kwargs={'pk': self.form.pk})
        self.client.login(username='user', password='password')

    def test_get_responds(self):
        response = self.client.get(self.advanced_url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_form_responds(self):
        response = self.client.post(self.advanced_url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('This field is required.', str(response.content))

    def test_valid_post(self):
        response = self.client.post(self.advanced_url, data={'name': 'foo', 'number': 1}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.form.advanced_settings.name, 'foo')

    def test_post_redirects(self):
        response = self.client.post(self.advanced_url, data={'name': 'foo', 'number': 1})
        url_helper = FormURLHelper(model=Form)
        self.assertRedirects(response, url_helper.index_url)
