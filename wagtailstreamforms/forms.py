from collections import OrderedDict

from django import forms
from django.utils.translation import gettext_lazy as _

from wagtailstreamforms.fields import get_fields


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")

        self.user = kwargs.pop("user", None)
        self.page = kwargs.pop("page", None)

        super().__init__(*args, **kwargs)


class FormBuilder:
    def __init__(self, fields):
        self.fields = fields

    @property
    def formfields(self):
        """Return a list of form fields from the registered fields."""

        formfields = OrderedDict()

        registered_fields = get_fields()

        for field in self.fields:
            field_type = field.get("type")
            field_value = field.get("value")

            # check we have the field
            if field_type not in registered_fields:
                raise AttributeError("Could not find a registered field of type %s" % field_type)

            # get the field
            registered_cls = registered_fields[field_type]()
            field_name = registered_cls.get_formfield_name(field_value)
            field_cls = registered_cls.get_formfield(field_value)
            formfields[field_name] = field_cls

        # add fields to uniquely identify the form
        formfields["form_id"] = forms.CharField(widget=forms.HiddenInput)
        formfields["form_reference"] = forms.CharField(widget=forms.HiddenInput)

        return formfields

    def get_form_class(self):
        return type(str("StreamformsForm"), (BaseForm,), self.formfields)


class SelectDateForm(forms.Form):
    date_from = forms.DateTimeField(
        required=False, widget=forms.DateInput(attrs={"placeholder": _("Date from")})
    )
    date_to = forms.DateTimeField(
        required=False, widget=forms.DateInput(attrs={"placeholder": _("Date to")})
    )
