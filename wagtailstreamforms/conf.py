from django.conf import settings
from django.utils.translation import ugettext_lazy as _


SETTINGS_PREFIX = 'WAGTAILSTREAMFORMS'
SETTINGS_DEFAULTS = {
    'ADMIN_MENU_LABEL': _('Streamforms'),
    'ADMIN_MENU_ORDER': None,
    'ADVANCED_SETTINGS_MODEL': None,
    'ENABLE_FORM_PROCESSING': True,
    'ENABLE_BUILTIN_HOOKS': True,
    'FORM_TEMPLATES': (
        ('streamforms/form_block.html', 'Default Form Template'),
    ),
    'DEFAULT_FIELDS': {
        'singleline': 'wagtailstreamforms.fields.SingleLineTextField',
        'multiline': 'wagtailstreamforms.fields.MultiLineTextField',
        'date': 'wagtailstreamforms.fields.DateField',
        'datetime': 'wagtailstreamforms.fields.DateTimeField',
        'email': 'wagtailstreamforms.fields.EmailField',
        'url': 'wagtailstreamforms.fields.URLField',
        'number': 'wagtailstreamforms.fields.NumberField',
        'dropdown': 'wagtailstreamforms.fields.DropdownField',
        'multiselect': 'wagtailstreamforms.fields.MultiSelectField',
        'radio': 'wagtailstreamforms.fields.RadioField',
        'checkboxes': 'wagtailstreamforms.fields.CheckboxesField',
        'checkbox': 'wagtailstreamforms.fields.CheckboxField',
        'hidden': 'wagtailstreamforms.fields.HiddenField',
        'singlefile': 'wagtailstreamforms.fields.SingleFileField',
        'multifile': 'wagtailstreamforms.fields.MultiFileField'
    }
}


def get_setting(name):
    setting_key = '{}_{}'.format(SETTINGS_PREFIX, name)
    return getattr(settings, setting_key, SETTINGS_DEFAULTS[name])
