from collections import OrderedDict

from django import forms

from wagtailstreamforms.fields import get_fields


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')

        self.user = kwargs.pop('user', None)
        self.page = kwargs.pop('page', None)

        super().__init__(*args, **kwargs)


class FormBuilder:

    def __init__(self, fields):
        self.fields = fields

    @property
    def formfields(self):
        """ Return a list of form fields from the registered fields. """

        formfields = OrderedDict()

        registered_fields = get_fields()

        for field in self.fields:
            registered_cls = registered_fields[field.field_type]()
            field_cls = registered_cls.get_formfield(field)
            formfields[field.clean_name] = field_cls

        # add fields to uniquely identify the form
        formfields['form_id'] = forms.CharField(widget=forms.HiddenInput)
        formfields['form_reference'] = forms.CharField(widget=forms.HiddenInput)

        return formfields

    def get_form_class(self):
        return type(str('StreamformsForm'), (BaseForm,), self.formfields)
