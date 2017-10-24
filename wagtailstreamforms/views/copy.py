from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView

from wagtail.contrib.modeladmin.helpers import PermissionHelper

from wagtailstreamforms.forms import CopyForm
from wagtailstreamforms.wagtail_hooks import FormURLHelper
from wagtailstreamforms.models import BaseForm


class CopyFormView(SingleObjectTemplateResponseMixin, BaseDetailView):
    model = BaseForm
    template_name = 'streamforms/confirm_copy.html'

    @property
    def permission_helper(self):
        return PermissionHelper(model=self.object.specific_class)

    @property
    def url_helper(self):
        return FormURLHelper(model=self.object.specific_class)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.permission_helper.user_can_create(self.request.user):
            raise PermissionDenied
        return super(CopyFormView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(CopyFormView, self).get_object(queryset)
        return obj.specific

    def copy(self, request, *args, **kwargs):
        form = CopyForm(request.POST)

        if form.is_valid():

            copied = self.object.copy()
            copied.name = form.cleaned_data['name']
            copied.save()

            return HttpResponseRedirect(self.get_success_url())

        context = self.get_context_data(object=self.object)
        context['form'] = form

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(object=self.object)
        context['form'] = CopyForm(initial={'name': self.object.name})

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.copy(request, *args, **kwargs)

    def get_success_url(self):
        return self.url_helper.index_url
