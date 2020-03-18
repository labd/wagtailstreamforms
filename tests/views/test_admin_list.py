from django.contrib.auth.models import User, Permission
from django.test import override_settings

from ..test_case import AppTestCase


class AdminListViewTestCase(AppTestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'password', is_staff=True)
        self.access_admin = Permission.objects.get(codename='access_admin')
        self.add_perm = Permission.objects.get(codename='add_form')
        self.change_perm = Permission.objects.get(codename='change_form')
        self.delete_perm = Permission.objects.get(codename='delete_form')
        self.client.login(username='user', password='password')

    def test_get_responds(self):
        self.user.user_permissions.add(self.access_admin, self.add_perm)
        response = self.client.get('/cms/wagtailstreamforms/form/')
        self.assertEqual(response.status_code, 200)

    def test_copy_button_uses_add_perm(self):
        self.user.user_permissions.add(self.access_admin, self.change_perm)

        response = self.client.get('/cms/wagtailstreamforms/form/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('title="Copy this form">Copy</a>', str(response.content))

        self.user.user_permissions.add(self.access_admin, self.add_perm)

        response = self.client.get('/cms/wagtailstreamforms/form/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('title="Copy this form">Copy</a>', str(response.content))

    @override_settings(WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL='tests.ValidFormSettingsModel')
    def test_advanced_button_enabled_when_setup(self):
        url = '/cms/wagtailstreamforms/form/'
        expected_html = 'title="Advanced settings">Advanced</a>'

        # disabled with delete perm
        self.user.user_permissions.add(self.access_admin, self.delete_perm)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(expected_html, str(response.content))

        # enabled with add perm
        self.user.user_permissions.remove(self.delete_perm)
        self.user.user_permissions.add(self.add_perm)

        response = self.client.get(url)
        self.assertIn(expected_html, str(response.content))

        # enabled with change perm
        self.user.user_permissions.remove(self.add_perm)
        self.user.user_permissions.add(self.change_perm)

        response = self.client.get(url)
        self.assertIn(expected_html, str(response.content))