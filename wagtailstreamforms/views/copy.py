from django import forms
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import (
    BaseDetailView,
    SingleObjectTemplateResponseMixin,
)
from wagtail_modeladmin.helpers import PermissionHelper

from wagtailstreamforms.models import Form
from wagtailstreamforms.wagtail_hooks import FormURLHelper


class CopyForm(forms.Form):
    title = forms.CharField(label=_("New title"))
    slug = forms.SlugField(label=_("New slug"))

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        if Form.objects.filter(slug=slug).exists():
            raise forms.ValidationError("This slug is already in use")
        return slug


class CopyFormView(SingleObjectTemplateResponseMixin, BaseDetailView):
    model = Form
    template_name = "streamforms/confirm_copy.html"
    success_message = _("Form '%s' copied to '%s'.")

    @property
    def permission_helper(self):
        return PermissionHelper(model=self.model)

    @property
    def url_helper(self):
        return FormURLHelper(model=self.model)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.permission_helper.user_can_create(self.request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

    def copy(self, request, *args, **kwargs):
        form = CopyForm(request.POST)

        if form.is_valid():
            copied = self.object.copy()
            copied.title = form.cleaned_data["title"]
            copied.slug = form.cleaned_data["slug"]

            copied.save()

            self.create_success_message(copied)

            return HttpResponseRedirect(self.get_success_url())

        context = self.get_context_data(object=self.object)
        context["form"] = form

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(object=self.object)
        context["form"] = CopyForm(initial={"title": self.object.title, "slug": self.object.slug})

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.copy(request, *args, **kwargs)

    def create_success_message(self, copied):
        success_message = self.success_message % (self.object, copied)
        messages.success(self.request, success_message)

    def get_success_url(self):
        return self.url_helper.index_url
