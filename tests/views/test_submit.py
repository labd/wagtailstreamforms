from django.urls import reverse

from wagtail_streamforms.models import BasicForm, FormField, FormSubmission

from ..test_case import AppTestCase


class SubmitViewTestCase(AppTestCase):

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

    # success path

    def test_post_responds(self):
        form = self.test_form()
        url = reverse('streamforms_submit', kwargs={'pk': form.pk})
        data = {'name': 'Bob'}
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)

    def test_post_response_is_json(self):
        form = self.test_form()
        url = reverse('streamforms_submit', kwargs={'pk': form.pk})
        data = {'name': 'Bob'}
        response = self.client.post(url, data)
        self.assertJSONEqual(str(response.content.decode("utf-8")), {'message': 'success'})

    def test_post_response_with_custom_message(self):
        form = self.test_form()
        form.success_message = 'Yay'
        form.save()
        url = reverse('streamforms_submit', kwargs={'pk': form.pk})
        data = {'name': 'Bob'}
        response = self.client.post(url, data)
        self.assertJSONEqual(str(response.content.decode("utf-8")), {'message': 'Yay'})

    def test_post_saves_submission(self):
        form = self.test_form(store_submission=True)
        url = reverse('streamforms_submit', kwargs={'pk': form.pk})
        data = {'name': 'Bob'}
        self.client.post(url, data)
        FormSubmission.objects.get(form=form)

    def test_post_doesnt_save_submission_when_not_required(self):
        form = self.test_form()
        url = reverse('streamforms_submit', kwargs={'pk': form.pk})
        data = {'name': 'Bob'}
        self.client.post(url, data)
        self.assertEquals(FormSubmission.objects.count(), 0)

    # error path

    def test_invalid_form_id_does_not_break_view(self):
        url = reverse('streamforms_submit', kwargs={'pk': 1000})
        data = {'name': 'Bob'}
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content.decode("utf-8")),
            {'message': 'error', 'detail': 'Could not find stream field form with id 1000'})

    def test_invalid_form_data_returns_errors(self):
        form = self.test_form()
        url = reverse('streamforms_submit', kwargs={'pk': form.pk})
        data = {'name': ''}
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content.decode("utf-8")),
            {'message': 'error', 'detail': {'name': ['This field is required.']}})
