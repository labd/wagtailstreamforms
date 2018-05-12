Form Submission Hooks
=====================

Form submission hooks are used to process the cleaned_data of the form after a successful post.
The only defined one is that to save the form submission data.

Example:

.. code-block:: python

    import json
    from django.core.serializers.json import DjangoJSONEncoder
    from wagtailstreamforms.hooks import register

    @register('process_form_submission')
    def save_form_submission_data(instance, form):
        """ saves the form submission data """

        instance.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            form=instance
        )

Create your own hook
--------------------

You can easily define additional hooks to perform a vast array of actions like

- send a mail
- save the data to a db
- reply to the sender
- etc

Here is a simple example to send an email with the subbmission data.

Create a ``wagtailstreamforms_hooks.py`` in the root of one of your apps and add the following.

.. code-block:: python

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

A new option will appear in the setup of the forms to run the above hook. The name of the option is taken from
the function name so keep them unique to avoid confusion. The ``instance`` is the form class instance, the
``form`` is the processed valid form in the request.
