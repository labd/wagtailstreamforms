from django.contrib.auth.models import User

from wagtailstreamforms.models import BasicForm

from ..test_case import AppTestCase


class AdminListViewTestCase(AppTestCase):
    fixtures = ['test.json']

    def setUp(self):
        User.objects.create_superuser('user', 'user@test.com', 'password')
        self.client.login(username='user', password='password')

    def test_get_responds(self):
        response = self.client.get('/cms/wagtailstreamforms/basicform/')
        self.assertEqual(response.status_code, 200)
