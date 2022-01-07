from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

from wagtailstreamforms.conf import get_setting
from wagtailstreamforms.models import AbstractFormSetting


def get_advanced_settings_model():
    """
    Returns the advanced form settings model if one is defined
    """

    model = get_setting("ADVANCED_SETTINGS_MODEL")

    if not model:
        return

    def raise_error(msg):
        setting = "WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL"
        raise ImproperlyConfigured("%s %s" % (setting, msg))

    try:
        model_class = apps.get_model(model, require_ready=False)
        if issubclass(model_class, AbstractFormSetting):
            return model_class
        raise_error("must inherit from 'wagtailstreamforms.models.AbstractFormSetting'")
    except ValueError:
        raise_error("must be of the form 'app_label.model_name'")
    except LookupError:
        raise_error("refers to model '%s' that has not been installed" % model)
