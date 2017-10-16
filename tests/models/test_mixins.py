from django.test.client import RequestFactory
from wagtail.wagtailcore.models import Page

from wagtailstreamforms.models import StreamFormPageMixin, BasicForm, FormField
from ..test_case import AppTestCase


class SomePage(StreamFormPageMixin, Page):
    class Meta:
        app_label = 'tests'


class TestPageServeMixin(AppTestCase):

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

    def test_get_responds(self):
        fake_request = self.rf.get('/fake/')

        response = SomePage().serve(fake_request)

        self.assertEquals(response.status_code, 200)

    def test_post_responds(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {'form_id': form.pk, 'name': 'Bill'})

        response = SomePage().serve(fake_request)

        self.assertEquals(response.status_code, 200)

    def test_post_saves_submission(self):
        form = self.test_form(True)
        fake_request = self.rf.post('/fake/', {'form_id': form.pk, 'name': 'Bill'})

        SomePage().serve(fake_request)

        self.assertEquals(form.get_submission_class().objects.count(), 1)

    def test_invalid_form_id_does_not_break_view(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {'form_id': 100})

        response = SomePage().serve(fake_request)

        self.assertEquals(response.status_code, 200)

    def test_no_form_id_does_not_break_view(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {})

        response = SomePage().serve(fake_request)

        self.assertEquals(response.status_code, 200)

    def test_invalid_data_does_not_break_view(self):
        form = self.test_form()
        fake_request = self.rf.post('/fake/', {'form_id': form.pk, 'name': ''})

        response = SomePage().serve(fake_request)

        self.assertEquals(response.status_code, 200)
