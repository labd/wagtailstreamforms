import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import QueryDict

from wagtailstreamforms.wagtailstreamforms_hooks import save_form_submission_data
from wagtailstreamforms.models import Form
from ..test_case import AppTestCase


class TestHook(AppTestCase):

    def test_form(self):
        form = Form.objects.create(
            title='Form',
            template_name='streamforms/form_block.html',
            slug='form',
            fields=json.dumps([
                {
                    "type": "singleline",
                    "value": {
                        "label": "singleline",
                        "required": True
                    },
                    "id": "9c46e208-e53a-4562-81f6-3fb3f34520f2"
                },
                {
                    "type": "multifile",
                    "value": {
                        "label": "multifile",
                        "required": True
                    },
                    "id": "91bac05f-754b-41a3-b038-ac7850e6f951"
                }
            ])
        )
        return form

    def test_saves_record_with_files(self):
        instance = self.test_form()

        data_dict = {
            'singleline': 'text',
            'form_id': instance.pk,
            'form_reference': 'some-ref'
        }
        files_dict = QueryDict(mutable=True)
        files_dict.update({'multifile': self.get_file()})
        files_dict.update({'multifile': self.get_file()})

        form_class = instance.get_form(data=data_dict, files=files_dict)

        assert form_class.is_valid()

        save_form_submission_data(instance, form_class)

        expected_data = {
            'singleline': 'text',
            'multifile': '2 files',
            'form_id': str(instance.pk),
            'form_reference': 'some-ref'
        }
        self.assertEqual(instance.get_submission_class().objects.count(), 1)
        self.assertDictEqual(json.loads(instance.get_submission_class().objects.all()[0].form_data), expected_data)
        self.assertEqual(instance.get_submission_class().objects.all()[0].files.count(), 2)
