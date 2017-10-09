from django.conf import settings


def recaptcha_enabled():
    return (
        'captcha' in settings.INSTALLED_APPS and
        getattr(settings, 'RECAPTCHA_PUBLIC_KEY', False) and
        getattr(settings, 'RECAPTCHA_PRIVATE_KEY', False)
    )
