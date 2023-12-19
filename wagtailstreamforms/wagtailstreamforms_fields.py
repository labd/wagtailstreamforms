from typing import List, Tuple

from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from wagtailstreamforms.conf import get_setting
from wagtailstreamforms.fields import BaseField, register


class SingleLineTextField(BaseField):
    field_class = forms.CharField
    label = _("Text field (single line)")


class MultiLineTextField(BaseField):
    field_class = forms.CharField
    widget = forms.widgets.Textarea
    label = _("Text field (multi line)")


class DateField(BaseField):
    field_class = forms.DateField
    icon = "date"
    label = _("Date field")


class DateTimeField(BaseField):
    field_class = forms.DateTimeField
    icon = "time"
    label = _("Time field")


class EmailField(BaseField):
    field_class = forms.EmailField
    icon = "mail"
    label = _("Email field")


class URLField(BaseField):
    field_class = forms.URLField
    icon = "link"
    label = _("URL field")


class NumberField(BaseField):
    field_class = forms.DecimalField
    label = _("Number field")


class DropdownField(BaseField):
    field_class = forms.ChoiceField
    icon = "arrow-down-big"
    label = _("Dropdown field")

    def get_options(self, block_value):
        options = super().get_options(block_value)
        choices: List[Tuple[str, str]] = []
        for c in block_value.get("choices"):
            if isinstance(c, dict) and c.get("value"):
                choices.append((c["value"].strip(), c["value"].strip()))
            else:
                choices.append((c.strip(), c.strip()))

        if block_value.get("empty_label"):
            choices.insert(0, ("", block_value.get("empty_label")))
        options.update({"choices": choices})
        return options

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
                ("empty_label", blocks.CharBlock(required=False)),
                ("choices", blocks.ListBlock(blocks.CharBlock(label="Option"))),
            ],
            icon=self.icon,
            label=self.label,
        )


class MultiSelectField(BaseField):
    field_class = forms.MultipleChoiceField
    icon = "list-ul"
    label = _("Multiselect field")

    def get_options(self, block_value):
        options = super().get_options(block_value)
        choices: List[Tuple[str, str]] = []
        for c in block_value.get("choices"):
            if isinstance(c, dict) and c.get("value"):
                choices.append((c["value"].strip(), c["value"].strip()))
            else:
                choices.append((c.strip(), c.strip()))
        options.update({"choices": choices})
        return options

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
                ("choices", blocks.ListBlock(blocks.CharBlock(label="Option"))),
            ],
            icon=self.icon,
            label=self.label,
        )


class RadioField(BaseField):
    field_class = forms.ChoiceField
    widget = forms.widgets.RadioSelect
    icon = "radio-empty"
    label = _("Radio buttons")

    def get_options(self, block_value):
        options = super().get_options(block_value)
        choices: List[Tuple[str, str]] = []
        for c in block_value.get("choices"):
            if isinstance(c, dict) and c.get("value"):
                choices.append((c["value"].strip(), c["value"].strip()))
            else:
                choices.append((c.strip(), c.strip()))
        options.update({"choices": choices})
        return options

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
                ("choices", blocks.ListBlock(blocks.CharBlock(label="Option"))),
            ],
            icon=self.icon,
            label=self.label,
        )


class CheckboxesField(BaseField):
    field_class = forms.MultipleChoiceField
    widget = forms.widgets.CheckboxSelectMultiple
    icon = "tick-inverse"
    label = _("Checkboxes")

    def get_options(self, block_value):
        options = super().get_options(block_value)
        choices: List[Tuple[str, str]] = []
        for c in block_value.get("choices"):
            if isinstance(c, dict) and c.get("value"):
                choices.append((c["value"].strip(), c["value"].strip()))
            else:
                choices.append((c.strip(), c.strip()))
        options.update({"choices": choices})
        return options

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
                ("choices", blocks.ListBlock(blocks.CharBlock(label="Option"))),
            ],
            icon=self.icon,
            label=self.label,
        )


class CheckboxField(BaseField):
    field_class = forms.BooleanField
    icon = "tick-inverse"
    label = _("Checkbox field")

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
            ],
            icon=self.icon,
            label=self.label,
        )


class HiddenField(BaseField):
    field_class = forms.CharField
    widget = forms.widgets.HiddenInput
    icon = "no-view"
    label = _("Hidden field")


class SingleFileField(BaseField):
    field_class = forms.FileField
    widget = forms.widgets.FileInput
    icon = "doc-full-inverse"
    label = _("File field")

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
            ],
            icon=self.icon,
            label=self.label,
        )


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if data and isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultiFileField(BaseField):
    field_class = MultipleFileField
    widget = MultipleFileInput(attrs={"multiple": True})
    icon = "doc-full-inverse"
    label = _("Files field")

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
            ],
            icon=self.icon,
            label=self.label,
        )


FIELD_MAPPING = {
    "singleline": SingleLineTextField,
    "multiline": MultiLineTextField,
    "date": DateField,
    "datetime": DateTimeField,
    "email": EmailField,
    "url": URLField,
    "number": NumberField,
    "dropdown": DropdownField,
    "radio": RadioField,
    "checkboxes": CheckboxesField,
    "checkbox": CheckboxField,
    "hidden": HiddenField,
    "singlefile": SingleFileField,
    "multifile": MultiFileField,
}

enabled_fields = get_setting("ENABLED_FIELDS")

for field_name in enabled_fields:
    cls = FIELD_MAPPING.get(field_name, None)
    if not cls:
        raise KeyError("Field with name '%s' does not exist" % field_name)
    register(field_name, cls)
