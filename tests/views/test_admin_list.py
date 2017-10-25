from django.contrib.auth.models import User

from wagtailstreamforms.models import BasicForm

from ..test_case import AppTestCase


class AdminListViewTestCase(AppTestCase):

    def setUp(self):
        User.objects.create_superuser('user', 'user@test.com', 'password')
        BasicForm.objects.create(name='Form', template_name='streamforms/form_block.html', slug='form')

        self.client.login(username='user', password='password')

    def test_get_responds(self):
        response = self.client.get('/cms/wagtailstreamforms/basicform/')
        self.assertEquals(response.status_code, 200)
