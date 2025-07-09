from django.conf import settings
from django.utils.translation import gettext_lazy as _

SETTINGS_PREFIX = "WAGTAILSTREAMFORMS"
SETTINGS_DEFAULTS = {
    "ADMIN_MENU_LABEL": _("Streamforms"),
    "ADMIN_MENU_ORDER": None,
    "ADVANCED_SETTINGS_MODEL": None,
    "ENABLE_FORM_PROCESSING": True,
    "ENABLE_BUILTIN_HOOKS": True,
    "ENABLED_FIELDS": (
        "singleline",
        "multiline",
        "date",
        "datetime",
        "email",
        "url",
        "number",
        "dropdown",
        "radio",
        "checkboxes",
        "checkbox",
        "hidden",
        "singlefile",
        "multifile",
    ),
    "FORM_TEMPLATES": [
        ("streamforms/form_block.html", "Default Form Template"),
    ],
}


def get_setting(name):
    setting_key = "{}_{}".format(SETTINGS_PREFIX, name)
    return getattr(settings, setting_key, SETTINGS_DEFAULTS[name])
