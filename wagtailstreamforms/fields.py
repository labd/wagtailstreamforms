from django import forms
from django.core import exceptions
from django.db import models
from django.utils.text import capfirst

from wagtail.core import blocks

from wagtailstreamforms import hooks
from wagtailstreamforms.utils import get_app_submodules


_fields = {}
_searched_for_fields = False


def register(field_name, cls=None):
    """
    Register field for ``field_name``. Can be used as a decorator::
        @register('singleline')
        class SingleLineTextField(BaseField):
            field_class = django.forms.CharField
    or as a function call::
        class SingleLineTextField(BaseField):
            field_class = django.forms.CharField
        register('singleline', SingleLineTextField)
    """

    if cls is None:
        def decorator(cls):
            register(field_name, cls)
            return cls
        return decorator

    _fields[field_name] = cls


def search_for_fields():
    global _searched_for_fields
    if not _searched_for_fields:
        list(get_app_submodules('wagtailstreamforms_fields'))
        _searched_for_fields = True


def get_fields():
    """ Return the registered field classes. """

    search_for_fields()
    return _fields


class BaseField:
    """ A base form field class """

    field_class = None
    widget = None
    icon = 'placeholder'

    def get_formfield(self, block_value):
        """ must return an instance of a form field class. """

        if not self.field_class:
            raise NotImplementedError('must provide a cls.field_class')

        options = self.get_options(block_value)

        if self.widget:
            return self.field_class(widget=self.widget, **options)

        return self.field_class(**options)

    def get_options(self, block_value):
        """ returns the default field options. """

        return {
            'label': block_value.get('label'),
            'help_text': block_value.get('help_text'),
            'required': block_value.get('required'),
            'initial': block_value.get('default_value')
        }

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('default_value', blocks.CharBlock(required=False)),
        ], icon=self.icon)


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
