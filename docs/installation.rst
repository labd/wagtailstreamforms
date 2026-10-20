Installation
============

Wagtail Streamforms is available on PyPI - to install it, just run:

.. code-block:: bash

    pip install wagtailstreamforms

or, in a project managed with `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: bash

    uv add wagtailstreamforms

Once thats done you need to add the following to your ``INSTALLED_APPS`` settings:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'wagtail_modeladmin',
        'generic_chooser',
        'wagtailstreamforms'
        ...
    ]

``generic_chooser`` provides the templates for the form chooser used by the form block,
without it the page editor raises ``TemplateDoesNotExist``.

Run migrations:

.. code-block:: bash

    python manage.py migrate

Go to your cms admin area and you will see the ``Streamforms`` section.

Compatibility
-------------

==================  ==============  ==========================  ===============
wagtailstreamforms  Wagtail         Django                      Python
==================  ==============  ==========================  ===============
5.3                 7.0 - 8.x       5.2, 6.0, 6.1               3.10 - 3.14
5.1 - 5.2           6.0 - 7.x       as supported by Wagtail     3.9+
==================  ==============  ==========================  ===============

The supported Django versions are those the installed Wagtail version supports;
Django 6.x requires Python 3.12 or newer.
