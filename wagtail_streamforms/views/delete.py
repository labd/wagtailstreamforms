from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ungettext
from django.views.generic import DeleteView

from wagtail_streamforms.models import BaseForm


class SubmissionDeleteView(DeleteView):
    model = BaseForm
    template_name = 'streamforms/confirm_delete.html'

    def get_submissions(self):
        submission_ids = self.request.GET.getlist('selected-submissions')
        return self.object.formsubmission_set.filter(id__in=submission_ids)

    def get_context_data(self, **kwargs):
        context = super(SubmissionDeleteView, self).get_context_data(**kwargs)
        context['submissions'] = self.get_submissions()
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        submissions = self.get_submissions()
        count = submissions.count()
        submissions.delete()
        self.create_success_message(count)
        return HttpResponseRedirect(success_url)

    def create_success_message(self, count):
        messages.success(
            self.request,
            ungettext(
                "One submission has been deleted.",
                "%(count)d submissions have been deleted.",
                count
            ) % {
                'count': count,
            }
        )

    def get_success_url(self):
        return reverse('streamforms_submissions', kwargs={'pk': self.object.pk})
