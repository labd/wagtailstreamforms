from django.apps import AppConfig
from django.conf import settings


SETTINGS_PREFIX = 'WAGTAILSTREAMFORMS'
SETTINGS_DEFAULTS = {
    'ADMIN_MENU_LABEL': 'Streamforms',
    'ADMIN_MENU_ORDER': None,
    'ENABLE_FORM_PROCESSING': True,
    'FORM_TEMPLATES': (
        ('streamforms/form_block.html', 'Default Form Template'),
    ),
}


def get_setting(name):
    setting_key = '{}_{}'.format(SETTINGS_PREFIX, name)
    return getattr(settings, setting_key, SETTINGS_DEFAULTS[name])


class StreamformsAppConf(AppConfig):
    name = 'wagtailstreamforms'
    verbose_name = 'Wagtail Streamforms'
