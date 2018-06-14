.. _hooks:

Submission Hooks
================

Form submission hooks are used to process the cleaned_data of the form after a successful post.
The only defined one is that to save the form submission data.

.. literalinclude:: ../wagtailstreamforms/wagtailstreamforms_hooks.py
   :pyobject: save_form_submission_data

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

    from django.core.mail import send_mail
    from wagtailstreamforms.hooks import register

    @register('process_form_submission')
    def email_submission(instance, form):
        """ Send an email with the submission. """

        addresses = ['to@example.com']
        content = ['Please see below submission\n', ]
        from_address = 'from@example.com'
        subject = 'New Submission'

        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field.label, value))
        content = '\n'.join(content)

        send_mail(subject, content, from_address, addresses, True)

A new option will appear in the setup of the forms to run the above hook. The name of the option is taken from
the function name so keep them unique to avoid confusion. The ``instance`` is the form class instance, the
``form`` is the processed valid form in the request.
