from django import forms
from wagtail.core import blocks

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
    icon = 'date'


@register('datetime')
class DateTimeField(BaseField):
    field_class = forms.DateTimeField
    icon = 'time'


@register('email')
class EmailField(BaseField):
    field_class = forms.EmailField
    icon = 'mail'


@register('url')
class URLField(BaseField):
    field_class = forms.URLField
    icon = 'link'


@register('number')
class NumberField(BaseField):
    field_class = forms.DecimalField


@register('dropdown')
class DropdownField(BaseField):
    field_class = forms.ChoiceField
    icon = 'list-ul'

    def get_options(self, block_value):
        options = super().get_options(block_value)
        choices = [(c.strip(), c.strip()) for c in block_value.get('choices')]
        if block_value.get('empty_label'):
            choices.insert(0, ('', block_value.get('empty_label')))
        options.update({'choices': choices})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('empty_label', blocks.CharBlock(required=False)),
            ('choices', blocks.ListBlock(blocks.CharBlock(label="Option"))),
        ], icon=self.icon)


@register('multiselect')
class MultiSelectField(BaseField):
    field_class = forms.MultipleChoiceField
    icon = 'list-ul'

    def get_options(self, block_value):
        options = super().get_options(block_value)
        choices = [(c.strip(), c.strip()) for c in block_value.get('choices')]
        options.update({'choices': choices})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('choices', blocks.ListBlock(blocks.CharBlock(label="Option"))),
        ], icon=self.icon)


@register('radio')
class RadioField(BaseField):
    field_class = forms.ChoiceField
    widget = forms.widgets.RadioSelect
    icon = 'radio-empty'

    def get_options(self, block_value):
        options = super().get_options(block_value)
        choices = [(c.strip(), c.strip()) for c in block_value.get('choices')]
        options.update({'choices': choices})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('choices', blocks.ListBlock(blocks.CharBlock(label="Option")))
        ], icon=self.icon)


@register('checkboxes')
class CheckboxesField(BaseField):
    field_class = forms.MultipleChoiceField
    widget = forms.widgets.CheckboxSelectMultiple
    icon = 'tick-inverse'

    def get_options(self, block_value):
        options = super().get_options(block_value)
        choices = [(c.strip(), c.strip()) for c in block_value.get('choices')]
        options.update({'choices': choices})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('choices', blocks.ListBlock(blocks.CharBlock(label="Option"))),
        ], icon=self.icon)


@register('checkbox')
class CheckboxField(BaseField):
    field_class = forms.BooleanField
    icon = 'tick-inverse'

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
        ], icon=self.icon)


@register('hidden')
class HiddenField(BaseField):
    field_class = forms.CharField
    widget = forms.widgets.HiddenInput
    icon = 'no-view'


@register('singlefile')
class SingleFileField(BaseField):
    field_class = forms.FileField
    widget = forms.widgets.FileInput
    icon = 'doc-full-inverse'


@register('multifile')
class MultiFileField(BaseField):
    field_class = forms.FileField
    widget = forms.widgets.FileInput(attrs={'multiple': True})
    icon = 'doc-full-inverse'
