from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ngettext
from django.views.generic import DeleteView
from wagtail_modeladmin.helpers import PermissionHelper

from wagtailstreamforms.models import Form


class SubmissionDeleteView(DeleteView):
    model = Form
    template_name = "streamforms/confirm_delete.html"

    @property
    def permission_helper(self):
        return PermissionHelper(model=self.model)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.permission_helper.user_can_delete_obj(self.request.user, self.object):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

    def get_submissions(self):
        submission_ids = self.request.GET.getlist("selected-submissions")
        submission_class = self.object.get_submission_class()
        return submission_class._default_manager.filter(id__in=submission_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submissions"] = self.get_submissions()
        return context

    def delete(self, request, *args, **kwargs):
        """
        Django 4.0 uses FormMixin, so this logic has been moved to form_valid.

        This can be removed once Django 3.2 is no longer supported.
        """
        success_url = self.get_success_url()
        submissions = self.get_submissions()
        count = submissions.count()
        submissions.delete()
        self.create_success_message(count)
        return HttpResponseRedirect(success_url)

    def form_valid(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        submissions = self.get_submissions()
        count = submissions.count()
        submissions.delete()
        self.create_success_message(count)
        return HttpResponseRedirect(success_url)

    def create_success_message(self, count):
        messages.success(
            self.request,
            ngettext(
                "One submission has been deleted.",
                "%(count)d submissions have been deleted.",
                count,
            )
            % {"count": count},
        )

    def get_success_url(self):
        return reverse("wagtailstreamforms:streamforms_submissions", kwargs={"pk": self.object.pk})
