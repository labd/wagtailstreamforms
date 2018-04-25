from django import forms

from wagtail.contrib.forms.forms import FormBuilder as OrigFormBuilder


class FormBuilder(OrigFormBuilder):

    def create_regex_field(self, field, options):
        """ The regex field """

        if field.regex_validator:
            # there is a selected validator so use it
            options.update({
                'regex': field.regex_validator.regex,
                'error_messages': {'invalid': field.regex_validator.error_message}
            })
        else:
            # otherwise allow anything
            options.update({'regex': '(.*?)'})

        return forms.RegexField(**options)

    @property
    def formfields(self):
        """ Add additional fields to the already defined ones """

        fields = super().formfields

        # add fields to uniquely identify the form
        fields['form_id'] = forms.CharField(widget=forms.HiddenInput)
        fields['form_reference'] = forms.CharField(widget=forms.HiddenInput)

        return fields
