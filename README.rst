Wagtail StreamForms
===================

|pypi| |tests| |github|

Allows you to build forms in the CMS admin area and add them to any StreamField in your site.
You can add your own fields along with the vast array of default fields which include the likes
of file fields. Form submissions are controlled by hooks that you can add that process the forms cleaned data.
Templates can be created which will then appear as choices when you build your form,
allowing you to display and submit a form however you want.

Installation
------------

.. code:: bash

    $ pip install wagtailstreamforms

or, in a project managed with `uv <https://docs.astral.sh/uv/>`_:

.. code:: bash

    $ uv add wagtailstreamforms

Then follow the `installation guide <https://wagtailstreamforms.readthedocs.io/en/latest/installation.html>`_.

Compatibility
-------------

==================  ==============  ==========================  ===============
wagtailstreamforms  Wagtail         Django                      Python
==================  ==============  ==========================  ===============
unreleased          7.0 - 8.x       5.2, 6.0, 6.1 [#django]_    3.12 - 3.14
5.3                 7.0 - 8.x       5.2, 6.0, 6.1 [#django]_    3.10 - 3.14
5.1 - 5.2           6.0 - 7.x       as supported by Wagtail     3.9+
==================  ==============  ==========================  ===============

.. [#django] Whichever of these the installed Wagtail version supports. Django 6.x requires Python 3.12+.

Backwards Compatibility
-----------------------

Please note that due to this package being virtually re-written for version 3, you cannot upgrade any existing
older version of this package to version 3 and onwards.
If you have an existing version installed less than 3 then you will need to completely remove it including
tables and any migrations that were applied in the databases ``django_migrations`` table.

Older versions:

If you are using a version of wagtail 1.x, then the latest compatible version of this package is 1.6.3:

.. code:: bash

    $ pip install wagtailstreamforms<2

Other wise you must install a version of this package from 2 onwards:

.. code:: bash

    $ pip install wagtailstreamforms>=2

What else is included?
----------------------

*  Each form is built using a StreamField.
*  Customise things like success and error messages, post submit redirects and more.
*  Forms are processed via a ``before_page_serve`` hook. Meaning there is no fuss like remembering to include a page mixin.
*  The hook can easily be disabled to provide the ability to create your own.
*  Form submissions are controlled via hooks meaning you can easily create things like emailing the submission which you can turn on and off on each form.
*  Fields can easily be added to the form from your own code such as Recaptcha or a Regex Field.
*  The default set of fields can easily be replaced to add things like widget attributes.
*  You can define a model that will allow you to save additional settings for each form.
*  Form submissions are also listed by their form which you can filter by date and are ordered by newest first.
*  Files can also be submitted to the forms that are shown with the form submissions.
*  A form and its fields can easily be copied to a new form.
*  There is a template tag that can be used to render a form, in case you want it to appear outside a StreamField.

Documentation
-------------

Can be found on `readthedocs <http://wagtailstreamforms.readthedocs.io/>`_.

Screenshots
-----------

.. figure:: http://wagtailstreamforms.readthedocs.io/en/latest/_images/screen_1.png
   :width: 728 px

   Example Front End

.. figure:: http://wagtailstreamforms.readthedocs.io/en/latest/_images/screen_3.png
   :width: 728 px

   Form Fields Selection

Development
-----------

The project is managed with `uv <https://docs.astral.sh/uv/>`_.

.. code:: bash

    $ git clone https://github.com/labd/wagtailstreamforms.git
    $ cd wagtailstreamforms
    $ make install   # uv sync --all-groups
    $ make test      # run the test suite against the locked versions
    $ make tox       # run the full Python/Django/Wagtail matrix via tox-uv
    $ make format    # ruff
    $ make docs      # build the Sphinx documentation

Example site with docker
------------------------

Clone the repo

.. code:: bash

    $ git clone https://github.com/labd/wagtailstreamforms.git

Run the docker container

.. code:: bash

    $ cd wagtailstreamforms
    $ docker-compose up

Create yourself a superuser

.. code:: bash

    $ docker-compose exec app bash
    $ python manage.py createsuperuser

Go to http://127.0.0.1:8000

.. |tests| image:: https://github.com/labd/wagtailstreamforms/actions/workflows/python-test.yml/badge.svg
   :target: https://github.com/labd/wagtailstreamforms/actions/workflows/python-test.yml
.. |pypi| image:: https://img.shields.io/pypi/v/wagtailstreamforms.svg
   :target: https://pypi.org/project/wagtailstreamforms/
.. |github| image:: https://img.shields.io/github/stars/labd/wagtailstreamforms.svg?style=social&logo=github
   :target: https://github.com/labd/wagtailstreamforms/stargazers

