from wagtail_streamforms.models import BaseForm, BasicForm

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(BasicForm, BaseForm))
