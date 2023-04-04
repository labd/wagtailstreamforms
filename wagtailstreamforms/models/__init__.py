from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .abstract import AbstractFormSetting  # noqa
from .file import FormSubmissionFile  # noqa
from .form import Form  # noqa
from .submission import FormSubmission  # noqa


def get_form_model_string():
    """
    Get the dotted ``app.Model`` name for the form model as a string.
    Useful for developers making Wagtail plugins that need to refer to the
    form model, such as in foreign keys, but the model itself is not required.
    """
    return getattr(settings, "WAGTAILSTREAMFORMS_FORM_MODEL", "wagtailstreamforms.Form")


def get_form_model():
    """
    Get the form model from the ``WAGTAILSTREAMFORMS_FORM_MODEL`` setting.
    Useful for developers making Wagtail plugins that need the form model.
    Defaults to the standard :class:`~wagtailstreamforms.Form` model
    if no custom model is defined.
    """
    from django.apps import apps

    model_string = get_form_model_string()
    try:
        return apps.get_model(model_string)
    except ValueError:
        raise ImproperlyConfigured(
            "WAGTAILSTREAMFORMS_FORM_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "WAGTAILSTREAMFORMS_FORM_MODEL refers to model '%s' that has not been installed"
            % model_string
        )
