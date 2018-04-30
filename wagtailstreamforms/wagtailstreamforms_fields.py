from django import forms

from wagtailstreamforms.fields import BaseField, register


@register('singleline')
class SingleLineTextField(BaseField):
    field_class = forms.CharField


@register('multiline')
class MultiLineTextField(BaseField):
    field_class = forms.CharField
    widget = forms.widgets.Textarea


@register('date')
class DateField(BaseField):
    field_class = forms.DateField


@register('datetime')
class DateTimeField(BaseField):
    field_class = forms.DateTimeField


@register('email')
class EmailField(BaseField):
    field_class = forms.EmailField


@register('url')
class URLField(BaseField):
    field_class = forms.URLField


@register('number')
class NumberField(BaseField):
    field_class = forms.DecimalField


@register('dropdown')
class DropdownField(BaseField):
    field_class = forms.ChoiceField

    def get_options(self, field):
        options = super().get_options(field)
        options.update({
            'choices': map(lambda x: (x.strip(), x.strip()), field.choices.split(','))
        })
        return options


@register('multiselect')
class MultiSelectField(BaseField):
    field_class = forms.MultipleChoiceField

    def get_options(self, field):
        options = super().get_options(field)
        options.update({
            'choices': map(lambda x: (x.strip(), x.strip()), field.choices.split(',')),
            'initial': [x.strip() for x in field.default_value.split(',')]
        })
        return options


@register('radio')
class RadioField(BaseField):
    field_class = forms.ChoiceField
    widget = forms.widgets.RadioSelect

    def get_options(self, field):
        options = super().get_options(field)
        options.update({
            'choices': map(lambda x: (x.strip(), x.strip()), field.choices.split(','))
        })
        return options


@register('checkboxes')
class CheckboxesField(BaseField):
    field_class = forms.MultipleChoiceField
    widget = forms.widgets.CheckboxSelectMultiple

    def get_options(self, field):
        options = super().get_options(field)
        options.update({
            'choices': [(x.strip(), x.strip()) for x in field.choices.split(',')],
            'initial': [x.strip() for x in field.default_value.split(',')]
        })
        return options


@register('checkbox')
class CheckboxField(BaseField):
    field_class = forms.BooleanField


@register('hidden')
class HiddenField(BaseField):
    field_class = forms.CharField
    widget = forms.widgets.HiddenInput
