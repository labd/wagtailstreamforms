from django import forms
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView

from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtailstreamforms.wagtail_hooks import FormURLHelper
from wagtailstreamforms.models import BaseForm


class CopyForm(forms.Form):
    name = forms.CharField(label=_('New name'))
    slug = forms.SlugField(label=_('New slug'))

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if BaseForm.objects.filter(slug=slug).exists():
            raise forms.ValidationError("This slug is already in use")
        return slug


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
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj.specific

    def copy(self, request, *args, **kwargs):
        form = CopyForm(request.POST)

        if form.is_valid():

            copied = self.object.copy()
            copied.name = form.cleaned_data['name']
            copied.slug = form.cleaned_data['slug']

            copied.save()

            return HttpResponseRedirect(self.get_success_url())

        context = self.get_context_data(object=self.object)
        context['form'] = form

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(object=self.object)
        context['form'] = CopyForm(initial={'name': self.object.name, 'slug': self.object.slug})

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.copy(request, *args, **kwargs)

    def get_success_url(self):
        return self.url_helper.index_url
