from django import forms
from django.core import exceptions
from django.db import models
from django.utils.text import capfirst

from wagtailstreamforms import hooks


class HookMultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple


class HookSelectField(models.Field):

    def get_choices_default(self):
        return [
            (fn.__name__, capfirst(fn.__name__.replace('_', ' ')))
            for fn in hooks.get_hooks('process_form_submission')
        ]

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if isinstance(value, str):
            return value
        elif isinstance(value, list):
            return ",".join(value)

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        defaults = {
            'form_class': HookMultiSelectFormField,
            'choices': self.get_choices_default()
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def from_db_value(self, value, expression, connection, context):
        if value is None or value == '':
            return []
        return value.split(',')

    def to_python(self, value):
        if not value or value == '':
            return []
        if isinstance(value, list):
            return value
        return value.split(',')

    def validate(self, value, model_instance):
        arr_choices = [v for v, s in self.get_choices_default()]
        for opt in value:
            if opt not in arr_choices:
                raise exceptions.ValidationError('%s is not a valid choice' % opt)
        return
