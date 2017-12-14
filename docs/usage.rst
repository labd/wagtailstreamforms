Basic Usage
===========

Just add the ``wagtailstreamforms.blocks.WagtailFormBlock()`` in any of your streamfields:

.. code-block:: python

    body = StreamField([
        ...
        ('form', WagtailFormBlock())
        ...
    ])

And you are ready to go.

Using the template tag
----------------------

There is also a template tag you can use outside of a streamfield, within a page.
All this is doing is rendering the form using the same block as in the streamfield.

The tag takes three parameters:

* **slug** (``string``) - The slug of the form instance.
* **reference** (``string``) - This should be a unique string and needs to be persistent on refresh/reload. See note below.
* **action** (``string``) optional - The form action url.

.. note:: The reference is used when the form is being validated.

    Because you can have any number of the same form on a page there needs to be a way of uniquely identifying the form beyond its ``PK``.
    This is so that when the form has validation errors and it is passed back through the pages context, We know what form it is.

    This reference **MUST** be persistent on page refresh or you will never see the errors.

Usage:

::

    {% load streamforms_tags %}
    {% streamforms_form slug="form-slug" reference="some-very-unique-reference" action="." %}

