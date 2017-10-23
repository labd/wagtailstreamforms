from django.conf import settings


def get_form_instance_from_request(request):
    """ Get the form class from the request. """
    from wagtailstreamforms.models import BaseForm
    form_id = request.POST.get('form_id')
    if form_id and form_id.isdigit():
        try:
            return BaseForm.objects.get(pk=int(form_id)).specific
        except BaseForm.DoesNotExist:
            pass
    return None


def get_valid_subclasses(cls):
    """ list all subclasses that are not abstract. """
    clss = []
    for subcls in cls.__subclasses__():
        if subcls._meta.abstract:
            continue  # pragma: no cover
        clss.append(subcls)
        sub_classes = get_valid_subclasses(subcls)
        if sub_classes:
            clss.extend(sub_classes)
    return clss


def recaptcha_enabled():
    return (
        'captcha' in settings.INSTALLED_APPS and
        getattr(settings, 'RECAPTCHA_PUBLIC_KEY', False) and
        getattr(settings, 'RECAPTCHA_PRIVATE_KEY', False)
    )
