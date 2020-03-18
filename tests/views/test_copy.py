from django.contrib.auth.models import User, Permission
from django.urls import reverse
from wagtailstreamforms.wagtail_hooks import FormURLHelper

from wagtailstreamforms.models import Form

from ..test_case import AppTestCase


class CopyViewTestCase(AppTestCase):
    fixtures = ['test.json']

    def setUp(self):
        User.objects.create_superuser('user', 'user@test.com', 'password')
        self.form = Form.objects.get(pk=1)

        self.copy_url = reverse('wagtailstreamforms:streamforms_copy', kwargs={'pk': self.form.pk})
        self.invalid_copy_url = reverse('wagtailstreamforms:streamforms_copy', kwargs={'pk': 100})

        self.client.login(username='user', password='password')

    def test_get_responds(self):
        response = self.client.get(self.copy_url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_form_responds(self):
        response = self.client.post(self.copy_url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('This field is required.', str(response.content))

    def test_invalid_form_slug_in_use_error(self):
        response = self.client.post(self.copy_url, data={'title': 'new copy', 'slug': self.form.slug})
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("This slug is already in use", str(response.content))

    def test_invalid_pk_raises_404(self):
        response = self.client.get(self.invalid_copy_url)
        self.assertEqual(response.status_code, 404)

    def test_post_copies(self):
        self.client.post(self.copy_url, data={'title': 'new copy', 'slug': 'new-slug'})
        self.assertEqual(Form.objects.count(), 2)

    def test_post_redirects(self):
        response = self.client.post(self.copy_url, data={'title': 'new copy', 'slug': 'new-slug'})
        url_helper = FormURLHelper(model=Form)
        self.assertRedirects(response, url_helper.index_url)


class CopyViewPermissionTestCase(AppTestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'password')
        form = Form.objects.get(pk=1)
        self.copy_url = reverse('wagtailstreamforms:streamforms_copy', kwargs={'pk': form.pk})

    def test_no_user_no_access(self):
        response = self.client.get(self.copy_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/cms/login/?next=/cms/wagtailstreamforms'))

    def test_user_with_no_perm_no_access(self):
        access_admin = Permission.objects.get(codename='access_admin')
        self.user.user_permissions.add(access_admin)

        self.client.login(username='user', password='password')

        response = self.client.get(self.copy_url)
        self.assertEqual(response.status_code, 403)

    def test_user_with_add_perm_has_access(self):
        access_admin = Permission.objects.get(codename='access_admin')
        form_perm = Permission.objects.get(codename='add_form')
        self.user.user_permissions.add(access_admin, form_perm)
        self.user.is_staff = True
        self.user.save()

        self.client.login(username='user', password='password')

        response = self.client.get(self.copy_url)
        self.assertEqual(response.status_code, 200)
