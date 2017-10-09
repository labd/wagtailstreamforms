from django import forms
from django.urls import reverse

from wagtail.wagtailcore import blocks

from wagtail_streamforms.models import BaseForm


class FormChooserBlock(blocks.ChooserBlock):
    target_model = BaseForm
    widget = forms.Select

    def value_for_form(self, value):
        if isinstance(value, self.target_model):
            return value.pk
        return value

    def to_python(self, value):
        if value is None:
            return value
        else:
            try:
                return self.target_model.objects.get_subclass(pk=value)
            except self.target_model.DoesNotExist:
                return None


class WagtailFormBlock(blocks.StructBlock):
    form = FormChooserBlock()

    class Meta:
        icon = 'icon icon-form'
        template = None

    def render(self, value, context=None):
        form = value['form']
        self.meta.template = form.template_name
        return super(WagtailFormBlock, self).render(value, context)

    def get_action_url(self, form):
        return reverse('streamforms_submit', kwargs={'pk': form.id})

    def get_context(self, value, parent_context=None):
        context = super(WagtailFormBlock, self).get_context(value, parent_context)
        form = value['form']
        context['form'] = form.get_form()
        context['form_id'] = form.id
        context['action_url'] = self.get_action_url(form)
        return context
