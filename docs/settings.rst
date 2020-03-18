Settings
========

Any settings with their defaults are listed below for quick reference.

.. code-block:: python

    # the label of the forms area in the admin sidebar
    WAGTAILSTREAMFORMS_ADMIN_MENU_LABEL = 'Streamforms'

    # the order of the forms area in the admin sidebar
    WAGTAILSTREAMFORMS_ADMIN_MENU_ORDER = None

    # the model defined to save advanced form settings
    # in the format of 'app_label.model_class'.
    # Model must inherit from 'wagtailstreamforms.models.AbstractFormSetting'.
    WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL = None

    # enable the built in hook to process form submissions
    WAGTAILSTREAMFORMS_ENABLE_FORM_PROCESSING = True

    # enable the built in hooks defined in wagtailstreamforms
    # currently (save_form_submission_data)
    WAGTAILSTREAMFORMS_ENABLE_BUILTIN_HOOKS = True

    # the default form template choices
    WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
        ('streamforms/form_block.html', 'Default Form Template'),
    )
