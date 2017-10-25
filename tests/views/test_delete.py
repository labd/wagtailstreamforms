from django.contrib.auth.models import User, Permission
from django.urls import reverse

from wagtailstreamforms.models import BasicForm, FormSubmission, EmailForm

from ..test_case import AppTestCase


class DeleteViewTestCase(AppTestCase):

    def setUp(self):
        User.objects.create_superuser('user', 'user@test.com', 'password')
        form = BasicForm.objects.create(name='Form', template_name='streamforms/form_block.html', slug='form')
        s1 = FormSubmission.objects.create(form=form, form_data='{"foo":1}')
        s2 = FormSubmission.objects.create(form=form, form_data='{"foo":1}')
        FormSubmission.objects.create(form=form, form_data='{"foo":1}')

        delete_url = reverse('streamforms_delete_submissions', kwargs={'pk': form.pk})

        self.invalid_delete_url = reverse('streamforms_delete_submissions', kwargs={'pk': 100})
        self.single_url = '{}?selected-submissions={}'.format(delete_url, s1.pk)
        self.multiple_url = '{}?selected-submissions={}&selected-submissions={}'.format(delete_url, s1.pk, s2.pk)
        self.redirect_url = reverse('streamforms_submissions', kwargs={'pk': form.pk})

        self.client.login(username='user', password='password')

    def test_get_responds(self):
        response = self.client.get(self.multiple_url)
        self.assertEquals(response.status_code, 200)

    def test_invalid_pk_raises_404(self):
        response = self.client.get(self.invalid_delete_url)
        self.assertEquals(response.status_code, 404)

    def test_get_context_has_submissions(self):
        response = self.client.get(self.multiple_url)
        self.assertEquals(response.context['submissions'].count(), 2)

    def test_get_response_confirm_text__plural(self):
        response = self.client.get(self.multiple_url)
        self.assertIn('Are you sure you want to delete these form submissions?', str(response.content))

    def test_get_response_confirm_text__singular(self):
        response = self.client.get(self.single_url)
        self.assertIn('Are you sure you want to delete this form submission?', str(response.content))

    def test_post_deletes(self):
        self.client.post(self.multiple_url)
        self.assertEquals(FormSubmission.objects.count(), 1)

    def test_post_redirects(self):
        response = self.client.post(self.multiple_url)
        self.assertRedirects(response, self.redirect_url)


class DeleteViewPermissionTestCase(AppTestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'password')

        self.basic_form = BasicForm.objects.create(
            name='Form',
            slug='basic-form',
            template_name='streamforms/form_block.html'
        )
        self.basic_form_submission = FormSubmission.objects.create(
            form=self.basic_form,
            form_data='{}'
        )
        self.email_form = EmailForm.objects.create(
            name='Form',
            slug='email-form',
            template_name='streamforms/form_block.html'
        )
        self.email_form_submission = FormSubmission.objects.create(
            form=self.email_form,
            form_data='{}'
        )

        self.basic_delete_url = '{}?selected-submissions={}'.format(
            reverse('streamforms_delete_submissions', kwargs={'pk': self.basic_form.pk}),
            self.basic_form_submission.pk
        )

        self.email_delete_url = '{}?selected-submissions={}'.format(
            reverse('streamforms_delete_submissions', kwargs={'pk': self.email_form.pk}),
            self.email_form_submission.pk
        )

    def test_no_user_no_access(self):
        response = self.client.get(self.basic_delete_url)
        self.assertEquals(response.status_code, 403)

        response = self.client.get(self.email_delete_url)
        self.assertEquals(response.status_code, 403)

    def test_user_with_no_perm_no_access(self):
        self.client.login(username='user', password='password')

        response = self.client.get(self.basic_delete_url)
        self.assertEquals(response.status_code, 403)

        response = self.client.get(self.email_delete_url)
        self.assertEquals(response.status_code, 403)

    def test_user_with_delete_perm_has_access(self):
        basic_form_perm = Permission.objects.get(codename='delete_basicform')
        email_form_perm = Permission.objects.get(codename='delete_emailform')
        self.user.user_permissions.add(basic_form_perm, email_form_perm)

        self.client.login(username='user', password='password')

        response = self.client.get(self.basic_delete_url)
        self.assertEquals(response.status_code, 200)

        response = self.client.get(self.email_delete_url)
        self.assertEquals(response.status_code, 200)

    def test_permissions_are_on_an_class_type_basis(self):
        basic_form_perm = Permission.objects.get(codename='delete_basicform')
        self.user.user_permissions.add(basic_form_perm)

        self.client.login(username='user', password='password')

        response = self.client.get(self.basic_delete_url)
        self.assertEquals(response.status_code, 200)

        # user should not be able to access this as they have no got
        # any delete_emailform perm
        response = self.client.get(self.email_delete_url)
        self.assertEquals(response.status_code, 403)
