from django import forms
from django.views.generic import UpdateView

from wagtailstreamforms.utils import get_advanced_settings_model
from wagtailstreamforms.wagtail_hooks import FormURLHelper
from wagtailstreamforms.models import Form


SettingsModel = get_advanced_settings_model()


class AdvancedSettingsForm(forms.ModelForm):
    class Meta:
        exclude = ('form',)
        model = SettingsModel


class AdvancedSettingsView(UpdateView):
    form_class = AdvancedSettingsForm
    model = SettingsModel
    template_name = 'streamforms/advanced_settings.html'

    @property
    def url_helper(self):
        return FormURLHelper(model=Form)

    def get_object(self, queryset=None):
        form = Form.objects.get(pk=self.kwargs.get('pk'))
        obj, created = self.model.objects.get_or_create(form=form)
        return obj

    def get_success_url(self):
        return self.url_helper.index_url
