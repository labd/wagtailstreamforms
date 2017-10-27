Installation
============

Wagtail Streamform is available on PyPI - to install it, just run:

.. code-block:: python
  
    pip install wagtailstreamforms

Once thats done you should add both ``wagtail.contrib.modeladmin`` and ``wagtailstreamforms`` to your ``INSTALLED_APPS`` settings:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'wagtail.contrib.modeladmin',
        'wagtailstreamforms'
        ...
    ]

Add the required urls:

.. code-block:: python

    from wagtailstreamforms import urls as streamforms_urls

    urlpatterns = [
        ...
        url(r'^streamforms/', include(streamforms_urls)),
        ...
    ]

Run migrations:

.. code-block:: bash

    python manage.py migrate

Go to your cms admin area and you will see the ``Streamforms`` section.
