import six

from django.db import models

from wagtailstreamforms.forms import MultiEmailField as MultiEmailFormField


class MultiEmailField(models.Field):
    description = "A multi e-mail field stored as a multi-lines text"

    def formfield(self, **kwargs):
        defaults = {'form_class': MultiEmailFormField}
        defaults.update(kwargs)
        return super(MultiEmailField, self).formfield(**defaults)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return []
        return value.splitlines()

    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, six.string_types):
            return value
        elif isinstance(value, list):
            return "\n".join(value)

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        return value.splitlines()

    def get_internal_type(self):
        return 'TextField'
