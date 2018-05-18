from datetime import timedelta

from django.core.management import call_command

from tests.test_case import AppTestCase
from wagtailstreamforms.models import FormSubmission, Form


class Tests(AppTestCase):
    fixtures = ['test']

    def test_command(self):
        form = Form.objects.get(pk=1)
        to_keep = FormSubmission.objects.create(form=form, form_data={})
        to_delete = FormSubmission.objects.create(form=form, form_data={})
        to_delete.submit_time = to_delete.submit_time - timedelta(days=2)
        to_delete.save()

        call_command('prunesubmissions', 1)

        FormSubmission.objects.get(pk=to_keep.pk)

        with self.assertRaises(FormSubmission.DoesNotExist):
            FormSubmission.objects.get(pk=to_delete.pk)
