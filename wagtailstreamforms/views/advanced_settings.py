from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.generic import UpdateView

from wagtailstreamforms.models import Form
from wagtailstreamforms.utils.loading import get_advanced_settings_model
from wagtailstreamforms.wagtail_hooks import FormURLHelper

SettingsModel = get_advanced_settings_model()


class AdvancedSettingsForm(forms.ModelForm):
    class Meta:
        exclude = ("form",)
        model = SettingsModel


class AdvancedSettingsView(UpdateView):
    form_class = AdvancedSettingsForm
    model = SettingsModel
    template_name = "streamforms/advanced_settings.html"
    success_message = _("Form '%s' advanced settings updated.")

    @property
    def url_helper(self):
        return FormURLHelper(model=Form)

    def get_object(self, queryset=None):
        form_pk = self.kwargs.get("pk")
        form = get_object_or_404(Form, pk=form_pk)

        try:
            obj = self.model.objects.get(form=form)
        except self.model.DoesNotExist:
            obj = self.model(form=form)

        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        self.create_success_message()
        return response

    def create_success_message(self):
        success_message = self.success_message % self.object.form
        messages.success(self.request, success_message)

    def get_success_url(self):
        return self.url_helper.index_url
