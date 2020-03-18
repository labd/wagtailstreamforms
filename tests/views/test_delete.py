from django.contrib.auth.models import Permission, User
from django.urls import reverse
from wagtailstreamforms.models import Form, FormSubmission

from ..test_case import AppTestCase


class DeleteViewTestCase(AppTestCase):
    fixtures = ["test.json"]

    def setUp(self):
        User.objects.create_superuser("user", "user@test.com", "password")
        form = Form.objects.get(pk=1)
        s1 = FormSubmission.objects.create(form=form, form_data='{"foo":1}')
        s2 = FormSubmission.objects.create(form=form, form_data='{"foo":1}')
        FormSubmission.objects.create(form=form, form_data='{"foo":1}')

        delete_url = reverse(
            "wagtailstreamforms:streamforms_delete_submissions", kwargs={"pk": form.pk}
        )

        self.invalid_delete_url = reverse(
            "wagtailstreamforms:streamforms_delete_submissions", kwargs={"pk": 100}
        )
        self.single_url = "{}?selected-submissions={}".format(delete_url, s1.pk)
        self.multiple_url = "{}?selected-submissions={}&selected-submissions={}".format(
            delete_url, s1.pk, s2.pk
        )
        self.redirect_url = reverse(
            "wagtailstreamforms:streamforms_submissions", kwargs={"pk": form.pk}
        )

        self.client.login(username="user", password="password")

    def test_get_responds(self):
        response = self.client.get(self.multiple_url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_pk_raises_404(self):
        response = self.client.get(self.invalid_delete_url)
        self.assertEqual(response.status_code, 404)

    def test_get_context_has_submissions(self):
        response = self.client.get(self.multiple_url)
        self.assertEqual(response.context["submissions"].count(), 2)

    def test_get_response_confirm_text__plural(self):
        response = self.client.get(self.multiple_url)
        self.assertIn(
            "Are you sure you want to delete these form submissions?",
            str(response.content),
        )

    def test_get_response_confirm_text__singular(self):
        response = self.client.get(self.single_url)
        self.assertIn(
            "Are you sure you want to delete this form submission?",
            str(response.content),
        )

    def test_post_deletes(self):
        self.client.post(self.multiple_url)
        self.assertEqual(FormSubmission.objects.count(), 1)

    def test_post_redirects(self):
        response = self.client.post(self.multiple_url)
        self.assertRedirects(response, self.redirect_url)


class DeleteViewPermissionTestCase(AppTestCase):
    fixtures = ["test.json"]

    def setUp(self):
        self.user = User.objects.create_user("user", "user@test.com", "password")

        self.form = Form.objects.get(pk=1)
        self.form_submission = FormSubmission.objects.create(
            form=self.form, form_data="{}"
        )

        self.delete_url = "{}?selected-submissions={}".format(
            reverse(
                "wagtailstreamforms:streamforms_delete_submissions",
                kwargs={"pk": self.form.pk},
            ),
            self.form_submission.pk,
        )

    def test_no_user_no_access(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url.startswith("/cms/login/?next=/cms/wagtailstreamforms")
        )

    def test_user_with_no_perm_no_access(self):
        access_admin = Permission.objects.get(codename="access_admin")
        self.user.user_permissions.add(access_admin)

        self.client.login(username="user", password="password")

        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)

    def test_user_with_delete_perm_has_access(self):
        access_admin = Permission.objects.get(codename="access_admin")
        form_perm = Permission.objects.get(codename="delete_form")
        self.user.user_permissions.add(access_admin, form_perm)

        self.client.login(username="user", password="password")

        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
