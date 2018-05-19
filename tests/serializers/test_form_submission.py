import json
from datetime import datetime, date

from django.contrib.auth.models import User

from tests.test_case import AppTestCase
from wagtailstreamforms.serializers import FormSubmissionSerializer


class TestSerializer(AppTestCase):

    def test_serialized(self):
        data_to_serialize = {
            "model": User(username="fred"),
            "model_multiple": [User(username="fred"), User(username="joe")],
            "date": date(2018, 1, 1),
            "datetime": datetime(2018, 1, 1),
            "list": [1, 2],
            "string": "foo",
            "integer": 1
        }
        expected_data = {
            "model": "fred",
            "model_multiple": ["fred", "joe"],
            "date": "2018-01-01",
            "datetime": "2018-01-01T00:00:00",
            "list": [1, 2],
            "string": "foo",
            "integer": 1
        }

        json_data = json.dumps(data_to_serialize, cls=FormSubmissionSerializer)

        self.assertEqual(json_data, json.dumps(expected_data))
