from django.contrib.auth.models import User, Permission
from django.urls import reverse
from wagtailstreamforms.wagtail_hooks import FormURLHelper

from wagtailstreamforms.models import BasicForm, EmailForm

from ..test_case import AppTestCase


class CopyViewTestCase(AppTestCase):

    def setUp(self):
        User.objects.create_superuser('user', 'user@test.com', 'password')
        form = BasicForm.objects.create(name='Form', template_name='streamforms/form_block.html')

        self.copy_url = reverse('streamforms_copy', kwargs={'pk': form.pk})
        self.invalid_copy_url = reverse('streamforms_copy', kwargs={'pk': 100})

        self.client.login(username='user', password='password')

    def test_get_responds(self):
        response = self.client.get(self.copy_url)
        self.assertEquals(response.status_code, 200)

    def test_invalid_form_responds(self):
        response = self.client.post(self.copy_url, data={})
        self.assertEquals(response.status_code, 200)
        self.assertInHTML('This field is required.', str(response.content))

    def test_invalid_pk_raises_404(self):
        response = self.client.get(self.invalid_copy_url)
        self.assertEquals(response.status_code, 404)

    def test_post_copies(self):
        self.client.post(self.copy_url, data={'name': 'new copy'})
        self.assertEquals(BasicForm.objects.count(), 2)

    def test_post_redirects(self):
        response = self.client.post(self.copy_url, data={'name': 'new copy'})
        url_helper = FormURLHelper(model=BasicForm)
        self.assertRedirects(response, url_helper.index_url)


class CopyViewPermissionTestCase(AppTestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'password')
        basic_form = BasicForm.objects.create(name='Form', template_name='streamforms/form_block.html')
        email_form = EmailForm.objects.create(name='Form', template_name='streamforms/form_block.html')
        self.basic_copy_url = reverse('streamforms_copy', kwargs={'pk': basic_form.pk})
        self.email_copy_url = reverse('streamforms_copy', kwargs={'pk': email_form.pk})

    def test_no_user_no_access(self):
        response = self.client.get(self.basic_copy_url)
        self.assertEquals(response.status_code, 403)

        response = self.client.get(self.email_copy_url)
        self.assertEquals(response.status_code, 403)

    def test_user_with_no_perm_no_access(self):
        self.client.login(username='user', password='password')

        response = self.client.get(self.basic_copy_url)
        self.assertEquals(response.status_code, 403)

        response = self.client.get(self.email_copy_url)
        self.assertEquals(response.status_code, 403)

    def test_user_with_add_perm_has_access(self):
        basic_form_perm = Permission.objects.get(codename='add_basicform')
        email_form_perm = Permission.objects.get(codename='add_emailform')
        self.user.user_permissions.add(basic_form_perm, email_form_perm)

        self.client.login(username='user', password='password')

        response = self.client.get(self.basic_copy_url)
        self.assertEquals(response.status_code, 200)

        response = self.client.get(self.email_copy_url)
        self.assertEquals(response.status_code, 200)
