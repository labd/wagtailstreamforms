from django.contrib.auth.models import User
from django.urls import reverse

from wagtailstreamforms.models import BasicForm, FormSubmission

from ..test_case import AppTestCase


class DeleteViewTestCase(AppTestCase):

    def setUp(self):
        User.objects.create_superuser('user', 'user@test.com', 'password')
        form = BasicForm.objects.create(name='Form', template_name='streamforms/form_block.html')
        s1 = FormSubmission.objects.create(form=form, form_data='{"foo":1}')
        s2 = FormSubmission.objects.create(form=form, form_data='{"foo":1}')
        FormSubmission.objects.create(form=form, form_data='{"foo":1}')

        delete_url = reverse('streamforms_delete_submissions', kwargs={'pk': form.pk})

        self.single_url = '{}?selected-submissions={}'.format(delete_url, s1.pk)
        self.multiple_url = '{}?selected-submissions={}&selected-submissions={}'.format(delete_url, s1.pk, s2.pk)
        self.redirect_url = reverse('streamforms_submissions', kwargs={'pk': form.pk})

        self.client.login(username='user', password='password')

    def test_get_responds(self):
        response = self.client.get(self.multiple_url)
        self.assertEquals(response.status_code, 200)

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
