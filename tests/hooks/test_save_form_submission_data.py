import json

from django.core.serializers.json import DjangoJSONEncoder

from wagtailstreamforms.wagtailstreamforms_hooks import save_form_submission_data
from wagtailstreamforms.models import Form
from ..test_case import AppTestCase


class TestHook(AppTestCase):

    def test_form(self):
        form = Form.objects.create(
            title='Form',
            template_name='streamforms/form_block.html',
            slug='form'
        )
        return form

    def test_saves_record(self):
        instance = self.test_form()
        data = {
            'singleline': 'text',
            'form_id': instance.pk,
            'form_reference': 'some-ref'
        }
        form_class = instance.get_form(data)
        assert form_class.is_valid()
        save_form_submission_data(instance, form_class)
        saved_form_data = json.dumps(form_class.cleaned_data, cls=DjangoJSONEncoder)
        self.assertEqual(instance.get_submission_class().objects.count(), 1)
        self.assertEqual(instance.get_submission_class().objects.all()[0].form_data, saved_form_data)
