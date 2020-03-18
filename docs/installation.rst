Installation
============

Wagtail Streamform is available on PyPI - to install it, just run:

.. code-block:: python
  
    pip install wagtailstreamforms

Once thats done you need to add the following to your ``INSTALLED_APPS`` settings:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'wagtail.contrib.modeladmin',
        'wagtailstreamforms'
        ...
    ]

Run migrations:

.. code-block:: bash

    python manage.py migrate

Go to your cms admin area and you will see the ``Streamforms`` section.
