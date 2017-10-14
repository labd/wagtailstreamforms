Installation
============

Wagtail Streamform is available on PyPI - to install it, just run:

::
  
    pip install wagtailstreamforms

Once thats done you should add ``wagtailstreamforms`` to your ``INSTALLED_APPS`` settings:

::

    INSTALLED_APPS = [
        ...
        'wagtailstreamforms'
        ...
    ]

Add the required urls:

::

    from wagtailstreamforms import urls as streamforms_urls

    urlpatterns = [
        ...
        url(r'^streamforms/', include(streamforms_urls)),
        ...
    ]

Run migrations:

::

    python manage.py migrate

Go to your cms admin area and you will see the ``Streamforms`` section.
