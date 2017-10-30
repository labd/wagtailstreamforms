from wagtailstreamforms.models import BasicForm, EmailForm, BaseForm
from wagtailstreamforms.utils import get_valid_subclasses

from ..test_case import AppTestCase


class TestCase(AppTestCase):

    def test_has_correct_subclasses(self):
        # does not include AbstractEmailForm
        self.assertListEqual(get_valid_subclasses(BaseForm), [BasicForm, EmailForm])
