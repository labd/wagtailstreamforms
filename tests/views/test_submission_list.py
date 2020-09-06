from datetime import datetime

from django.contrib.auth.models import Permission, User
from django.urls import reverse

from wagtailstreamforms.models import Form, FormSubmission

from ..test_case import AppTestCase


class SubmissionListViewTestCase(AppTestCase):
    fixtures = ["test.json"]

    def setUp(self):
        User.objects.create_superuser("user", "user@test.com", "password")
        form = Form.objects.get(pk=1)
        s1 = FormSubmission.objects.create(form=form, form_data='{"foo":1}')
        s1.submit_time = datetime(2017, 1, 1, 0, 0, 0, 0)
        s1.save()
        s2 = FormSubmission.objects.create(form=form, form_data='{"foo":1}')
        s2.submit_time = datetime(2017, 1, 2, 10, 0, 0, 0)
        s2.save()
        FormSubmission.objects.create(form=form, form_data='{"foo":1}')

        self.list_url = reverse(
            "wagtailstreamforms:streamforms_submissions", kwargs={"pk": form.pk}
        )
        self.invalid_list_url = reverse(
            "wagtailstreamforms:streamforms_submissions", kwargs={"pk": 100}
        )
        self.filter_url = (
            "{}?date_from=2017-01-01&date_to=2017-01-02&action=filter".format(
                self.list_url
            )
        )
        self.invalid_filter_url = "{}?date_from=xx&date_to=xx&action=filter".format(
            self.list_url
        )
        self.csv_url = "{}?date_from=2017-01-01&date_to=2017-01-02&action=CSV".format(
            self.list_url
        )

        self.client.login(username="user", password="password")

    def test_get_responds(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_pk_raises_404(self):
        response = self.client.get(self.invalid_list_url)
        self.assertEqual(response.status_code, 404)

    def test_get_context(self):
        response = self.client.get(self.list_url)
        self.assertIn("filter_form", response.context)
        self.assertIn("data_rows", response.context)
        self.assertIn("data_headings", response.context)
        self.assertEqual(len(response.context["data_rows"]), 3)

    def test_get_filtering(self):
        response = self.client.get(self.filter_url)
        self.assertEqual(len(response.context["data_rows"]), 2)

    def test_get_filtering_doesnt_happen_with_invalid_form(self):
        response = self.client.get(self.invalid_filter_url)
        self.assertEqual(len(response.context["data_rows"]), 3)

    def test_get_csv(self):
        response = self.client.get(self.csv_url)
        self.assertEqual(
            response.get("Content-Disposition"), "attachment;filename=export.csv"
        )


class ListViewPermissionTestCase(AppTestCase):
    fixtures = ["test.json"]

    def setUp(self):
        self.user = User.objects.create_user("user", "user@test.com", "password")
        self.form = Form.objects.get(pk=1)
        self.list_url = reverse(
            "wagtailstreamforms:streamforms_submissions", kwargs={"pk": self.form.pk}
        )

    def test_no_user_no_access(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url.startswith("/cms/login/?next=/cms/wagtailstreamforms")
        )

    def test_user_with_no_perm_no_access(self):
        access_admin = Permission.objects.get(codename="access_admin")
        self.user.user_permissions.add(access_admin)

        self.client.login(username="user", password="password")

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)

    def test_user_with_add_perm_has_access(self):
        access_admin = Permission.objects.get(codename="access_admin")
        form_perm = Permission.objects.get(codename="add_form")
        self.user.user_permissions.add(access_admin, form_perm)
        self.user.is_staff = True
        self.user.save()

        self.client.login(username="user", password="password")

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_user_with_change_perm_has_access(self):
        access_admin = Permission.objects.get(codename="access_admin")
        form_perm = Permission.objects.get(codename="change_form")
        self.user.user_permissions.add(access_admin, form_perm)
        self.user.is_staff = True
        self.user.save()

        self.client.login(username="user", password="password")

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_user_with_delete_perm_has_access(self):
        access_admin = Permission.objects.get(codename="access_admin")
        form_perm = Permission.objects.get(codename="delete_form")
        self.user.user_permissions.add(access_admin, form_perm)
        self.user.is_staff = True
        self.user.save()

        self.client.login(username="user", password="password")

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
