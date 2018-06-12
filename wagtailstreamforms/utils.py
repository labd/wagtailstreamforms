from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from unidecode import unidecode

from django.apps import apps
from django.utils.module_loading import module_has_submodule
from django.utils.text import slugify

from wagtailstreamforms.conf import get_setting
from wagtailstreamforms.models.abstract import AbstractFormSetting


def get_advanced_settings_model():
    """
    Returns the advanced form settings model if one is defined
    """

    model = get_setting('ADVANCED_SETTINGS_MODEL')

    if not model:
        return

    def raise_error(msg):
        setting = 'WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL'
        raise ImproperlyConfigured('%s %s' % (setting, msg))

    try:
        model_class = apps.get_model(model, require_ready=False)
        if issubclass(model_class, AbstractFormSetting):
            return model_class
        raise_error("must inherit from 'wagtailstreamforms.models.AbstractFormSetting'")
    except ValueError:
        raise_error("must be of the form 'app_label.model_name'")
    except LookupError:
        raise_error("refers to model '%s' that has not been installed" % model)


def get_app_modules():
    """
    Generator function that yields a module object for each installed app
    yields tuples of (app_name, module)
    """

    for app in apps.get_app_configs():
        yield app.name, app.module


def get_app_submodules(submodule_name):
    """
    Searches each app module for the specified submodule
    yields tuples of (app_name, module)
    """

    for name, module in get_app_modules():
        if module_has_submodule(module, submodule_name):
            yield name, import_module('%s.%s' % (name, submodule_name))


def get_form_instance_from_request(request):
    """ Get the form class from the request. """

    from wagtailstreamforms.models import Form
    form_id = request.POST.get('form_id')
    if form_id and form_id.isdigit():
        try:
            return Form.objects.get(pk=int(form_id))
        except Form.DoesNotExist:
            pass
    return None


def get_slug_from_string(label):
    return str(slugify(str(unidecode(label))))
