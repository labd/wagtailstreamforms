from django.conf import settings
from django.core.mail import send_mail

from wagtailstreamforms.hooks import register


@register('process_form_submission')
def email_submission(instance, form):
    """ Send an email with the submission. """

    if not hasattr(instance, 'advanced_settings'):
        return

    addresses = [instance.advanced_settings.to_address]
    content = ['Please see below submission\n', ]
    from_address = settings.DEFAULT_FROM_EMAIL
    subject = 'New Form Submission : %s' % instance.title

    for field in form:
        value = field.value()
        if isinstance(value, list):
            value = ', '.join(value)
        content.append('{}: {}'.format(field.label, value))
    content = '\n'.join(content)

    send_mail(subject, content, from_address, addresses, True)
