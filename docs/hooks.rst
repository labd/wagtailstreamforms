.. _hooks:

Submission Hooks
================

Form submission hooks are used to process the cleaned_data of the form after a successful post.
The only defined one is that to save the form submission data.

.. literalinclude:: ../wagtailstreamforms/wagtailstreamforms_hooks.py
   :pyobject: save_form_submission_data

You can disable this by setting ``WAGTAILSTREAMFORMS_ENABLE_BUILTIN_HOOKS=False`` in your ``settings.py``

Create your own hook
--------------------

You can easily define additional hooks to perform a vast array of actions like

- send a mail
- save the data to a db
- reply to the sender
- etc

Here is a simple example to send an email with the submission data.

Create a ``wagtailstreamforms_hooks.py`` in the root of one of your apps and add the following.

.. code-block:: python

    from django.conf import settings
    from django.core.mail import EmailMessage
    from django.template.defaultfilters import pluralize

    from wagtailstreamforms.hooks import register

    @register('process_form_submission')
    def email_submission(instance, form):
        """ Send an email with the submission. """

        addresses = ['to@example.com']
        content = ['Please see below submission\n', ]
        from_address = settings.DEFAULT_FROM_EMAIL
        subject = 'New Form Submission : %s' % instance.title

        # build up the email content
        for field, value in form.cleaned_data.items():
            if field in form.files:
                count = len(form.files.getlist(field))
                value = '{} file{}'.format(count, pluralize(count))
            elif isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field, value))
        content = '\n'.join(content)

        # create the email message
        email = EmailMessage(
            subject=subject,
            body=content,
            from_email=from_address,
            to=addresses
        )

        # attach any files submitted
        for field in form.files:
            for file in form.files.getlist(field):
                file.seek(0)
                email.attach(file.name, file.read(), file.content_type)

        # finally send the email
        email.send(fail_silently=True)

A new option will appear in the setup of the forms to run the above hook. The name of the option is taken from
the function name so keep them unique to avoid confusion. The ``instance`` is the form class instance, the
``form`` is the processed valid form in the request.
