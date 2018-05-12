from django.core.mail import send_mail

from wagtailstreamforms.hooks import register

@register('process_form_submission')
def email_bob_with_submission(instance, form):
    """ Send an email to bob with the submission. """

    content = [
        'Please see below submission\n',
    ]

    for name, field in form.fields.items():
        data = form.cleaned_data.get(name)
        label = field.label or name
        content.append(label + ': ' + str(data))

    send_mail(
        'New Submission',
        '\n'.join(content),
        'from@example.com',
        ['bob@example.com'],
        True
    )
