from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField
from wagtail.wagtailforms.forms import FormBuilder as OrigFormBuilder
from wagtailstreamforms.utils import recaptcha_enabled
from wagtailstreamforms.widgets import MultiEmailWidget


class FormBuilder(OrigFormBuilder):

    def __init__(self, fields, **kwargs):
        self.add_recaptcha = kwargs.pop('add_recaptcha')
        super(FormBuilder, self).__init__(fields)

    def create_regex_field(self, field, options):
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

    # doing this here rather than init as although works test are failing all over the place
    OrigFormBuilder.FIELD_TYPES.update({'regexfield': create_regex_field})

    @property
    def formfields(self):
        fields = super(FormBuilder, self).formfields

        # add form id to identify the form type
        fields['form_id'] = forms.CharField(widget=forms.HiddenInput)
        fields['form_reference'] = forms.CharField(widget=forms.HiddenInput)

        # if enabled add recaptcha field
        if self.add_recaptcha and recaptcha_enabled():
            fields['recaptcha'] = ReCaptchaField(label='')

        return fields


class MultiEmailField(forms.Field):
    message = _('Enter valid email addresses.')
    code = 'invalid'
    widget = MultiEmailWidget

    def to_python(self, value):
        """ Normalize data to a list of strings. """

        if not value:
            return []
        return [v.strip() for v in value.splitlines() if v != '']

    def validate(self, value):
        """ Check if value consists only of valid emails. """

        super(MultiEmailField, self).validate(value)
        try:
            for email in value:
                validate_email(email)
        except ValidationError:
            raise ValidationError(self.message, code=self.code)
