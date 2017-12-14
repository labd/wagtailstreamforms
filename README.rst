Wagtail StreamForms
===================

|CircleCI| |Codecov|

Allows you to build forms in the CMS admin area and add them to any StreamField in your site.
You can create your own types of forms meaning an endless array of possibilities. Templates can be created
which will then appear as choices when you build your form, allowing you to display and submit a form however you want.

What else is included?
----------------------

*  Customise things like success and error messages, post submit redirects and more.
*  Forms are processed via a ``before_page_serve`` hook. Meaning there is no fuss like remembering to include a page mixin.
*  The hook can easily be disabled to provide the ability to create your own.
*  Forms are categorised by their class in the CMS admin for easier navigation.
*  Form submissions are also listed by their form which you can filter by date and are ordered by newest first.
*  You can add site wide regex validators for use in regex fields.
*  A form and its fields can easily be copied to a new form.
*  There is a template tag that can be used to render a form, in case you want it to appear outside a StreamField.
*  Recaptcha can be added to a form.

Documentation
-------------

Can be found on `readthedocs <http://wagtailstreamforms.readthedocs.io/>`_.

Screenshots
-----------

.. figure:: http://wagtailstreamforms.readthedocs.io/en/latest/_images/screen7.png
   :width: 728 px

   Example Front End

.. figure:: http://wagtailstreamforms.readthedocs.io/en/latest/_images/screen1.png
   :width: 728 px

   Menu

Example site with docker
------------------------

Clone the repo

.. code:: bash

    $ git clone https://github.com/AccentDesign/wagtailstreamforms.git

Run the docker container

.. code:: bash

    $ cd wagtailstreamforms
    $ docker-compose up

Create yourself a superuser

.. code:: bash

    $ docker exec -it <container_name> bash
    $ python manage.py createsuperuser

Go to http://127.0.0.1:8000

Testing
-------

Install dependencies

You will need pyenv installed see https://github.com/pyenv/pyenv

Also tox needs to be installed

.. code:: bash

    $ pip install tox

Install python versions in pyenv

.. code:: bash

    $ pyenv install 3.4.4
    $ pyenv install 3.5.3
    $ pyenv install 3.6.2

Set local project versions

.. code:: bash

    $ pyenv local 3.4.4 3.5.3 3.6.2

Run the tests

.. code:: bash

    $ tox

or run for a single environment

.. code:: bash

    $ tox -e py36-dj111-wt112

.. |CircleCI| image:: https://circleci.com/gh/AccentDesign/wagtailstreamforms/tree/master.svg?style=svg
   :target: https://circleci.com/gh/AccentDesign/wagtailstreamforms/tree/master
.. |Codecov| image:: https://codecov.io/gh/AccentDesign/wagtailstreamforms/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/AccentDesign/wagtailstreamforms
