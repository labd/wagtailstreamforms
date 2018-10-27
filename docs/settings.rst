.. _settings:

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

    # the default set of fields loaded from the package
    # override this to remove unrequired fields
    WAGTAILSTREAMFORMS_DEFAULT_FIELDS = {
        'singleline': 'wagtailstreamforms.fields.SingleLineTextField',
        'multiline': 'wagtailstreamforms.fields.MultiLineTextField',
        'date': 'wagtailstreamforms.fields.DateField',
        'datetime': 'wagtailstreamforms.fields.DateTimeField',
        'email': 'wagtailstreamforms.fields.EmailField',
        'url': 'wagtailstreamforms.fields.URLField',
        'number': 'wagtailstreamforms.fields.NumberField',
        'dropdown': 'wagtailstreamforms.fields.DropdownField',
        'multiselect': 'wagtailstreamforms.fields.MultiSelectField',
        'radio': 'wagtailstreamforms.fields.RadioField',
        'checkboxes': 'wagtailstreamforms.fields.CheckboxesField',
        'checkbox': 'wagtailstreamforms.fields.CheckboxField',
        'hidden': 'wagtailstreamforms.fields.HiddenField',
        'singlefile': 'wagtailstreamforms.fields.SingleFileField',
        'multifile': 'wagtailstreamforms.fields.MultiFileField'
    }
