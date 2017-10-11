from django.contrib.auth.models import User

from wagtail_streamforms.models import BasicForm

from ..test_case import AppTestCase


class AdminListViewTestCase(AppTestCase):

    def setUp(self):
        User.objects.create_superuser('user', 'user@test.com', 'password')
        BasicForm.objects.create(name='Form', template_name='streamforms/form_block.html')

        self.client.login(username='user', password='password')

    def test_get_responds(self):
        response = self.client.get('/cms/wagtail_streamforms/basicform/')
        self.assertEquals(response.status_code, 200)
