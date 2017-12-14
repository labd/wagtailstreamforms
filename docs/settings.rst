Settings
========

Any settings with their defaults are listed below for quick reference.

.. code-block:: python

    # the label of the forms area in the admin sidebar
    WAGTAILSTREAMFORMS_ADMIN_MENU_LABEL = 'Streamforms'

    # the order of the forms area in the admin sidebar
    WAGTAILSTREAMFORMS_ADMIN_MENU_ORDER = None

    # enable the built in hook to process form submissions
    WAGTAILSTREAMFORMS_ENABLE_FORM_PROCESSING = True

    # the default form template choices
    WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
        ('streamforms/form_block.html', 'Default Form Template'),
    )
