Advanced Settings
=================

Some times there is a requirement to save additional data for each form.
Such as details of where to email the form submission. When this is needed we have
provided the means to define your own model.

To enable this you need to declare a model that inherits from
``wagtailstreamforms.models.AbstractFormSetting``:

.. code-block:: python
  
    from wagtailstreamforms.models.abstract import AbstractFormSetting

    class AdvancedFormSetting(AbstractFormSetting):
        to_address = models.EmailField()

Once that's done you need to add a setting to point to that model:

.. code-block:: python

    # the model defined to save advanced form settings
    # in the format of 'app_label.model_class'.
    # Model must inherit from 'wagtailstreamforms.models.AbstractFormSetting'.
    WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL = 'myapp.AdvancedFormSetting'

A button will appear on the Streamforms listing view ``Advanced`` which will
allow you to edit that model.

Usage
-----

The data saved can be used in :ref:`hooks` on the ``instance.advanced_settings`` property.

.. code-block:: python

    @register('process_form_submission')
    def email_submission(instance, form):
        send_mail(
            ..
            recipient_list=[instance.advanced_settings.to_address]
        )