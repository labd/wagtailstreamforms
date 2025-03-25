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

        for field in self.fields:
            field_name, field_cls = self.create_field_class(field)
            formfields[field_name] = field_cls

        # add fields to uniquely identify the form
        formfields["form_id"] = forms.CharField(widget=forms.HiddenInput)
        formfields["form_reference"] = forms.CharField(widget=forms.HiddenInput)

        return formfields

    def create_field_class(self, field):
        """
        Encapsulates the field_cls creation such that there is a method to override
        when the field_cls needs to be modified.

        :param field: StreamBlock representing a form field; an item in
        fields.stream_data
        :return: a tuple of field_name - the name to use in the html form for this
        field, and field_cls - in instantiated field class that may be added to a form
        """
        registered_fields = get_fields()

        field_type = field.get("type")
        field_value = field.get("value")
        # check we have the field
        if field_type not in registered_fields:
            raise AttributeError(
                "Could not find a registered field of type %s" % field_type
            )

        # get the field
        registered_cls = registered_fields[field_type]()
        field_cls = registered_cls.get_formfield(field_value)
        field_name = self.create_field_name(registered_cls, field)
        return field_name, field_cls

    def create_field_name(self, registered_cls, field):
        """
        Encapsulates the field_name creation such that there is a method to override
        when the field_name needs to be modified.

        :param field: StreamBlock representing a form field; an item in
        fields.stream_data
        :param registered_cls: The subclass of wagtailstreamforms.fields.BaseField
        that defined this form field
        :return: a name to use in the html form for this field
        """
        return registered_cls.get_formfield_name(field.get("value"))

    def get_form_class(self):
        return type(str("StreamformsForm"), (BaseForm,), self.formfields)


class SelectDateForm(forms.Form):
    date_from = forms.DateTimeField(
        required=False, widget=forms.DateInput(attrs={"placeholder": _("Date from")})
    )
    date_to = forms.DateTimeField(
        required=False, widget=forms.DateInput(attrs={"placeholder": _("Date to")})
    )
