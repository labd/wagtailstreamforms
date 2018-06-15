from django import forms
from django.contrib.auth.models import User

from captcha.fields import ReCaptchaField
from wagtail.core import blocks
from wagtailstreamforms.fields import BaseField, register


@register('recaptcha')
class ReCaptchaField(BaseField):
    field_class = ReCaptchaField
    icon = 'success'
    label = 'ReCAPTCHA field'

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({
            'required': True
        })
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
        ], icon=self.icon, label=self.label)


@register('regex_validated')
class RegexValidatedField(BaseField):
    field_class = forms.RegexField
    label = 'Regex field'

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({
            'regex': block_value.get('regex'),
            'error_messages': {'invalid': block_value.get('error_message')}
        })
        return options

    def get_regex_choices(self):
        return (
            ('(.*?)', 'Any'),
            ('^[a-zA-Z0-9]+$', 'Letters and numbers only'),
        )

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('regex', blocks.ChoiceBlock(choices=self.get_regex_choices())),
            ('error_message', blocks.CharBlock()),
            ('default_value', blocks.CharBlock(required=False)),
        ], icon=self.icon, label=self.label)


@register('user')
class UserChoiceField(BaseField):
    field_class = forms.ModelChoiceField
    icon = 'user'
    label = 'User dropdown field'

    @staticmethod
    def get_queryset():
        return User.objects.all()

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'queryset': self.get_queryset()})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
        ], icon=self.icon, label=self.label)
