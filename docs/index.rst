.. Wagtail Streamforms documentation master file, created by
   sphinx-quickstart on Sat Oct 14 14:40:45 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Wagtail Streamforms
===================

Allows you to built forms in the cms admin area and add them to any streamfield in your site.
You can create your own types of forms meaning an endless array of possibilities. Templates can be created
which will then appear as choices when you build your form. Allowing you to display and submit a form however you want.

What else is included?
----------------------

*  Customise things like success and error messages, post submit redirects and more.
*  Forms are processed via a ``before_page_serve`` hook. Meaning there is no fuss like remembering to include a page mixin.
*  The hook can easily be disabled to provide the ability to create your own.
*  Forms are catagorised by their class in the cms admin for easier navigation.
*  Form submissions are also listed by their form which you can filter by date and are ordered by newest first.
*  You can add site wide regex validators for use in regex fields.
*  A form and it's fields can easily be copied to a new form.
*  There is a template tag that can be used to render a form. Incase you want it to appear outside a streamfield.
*  Recaptcha can be added to a form.


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   installation
   usage
   templates
   forms
   submission
   permissions
   recaptcha
   settings
   screenshots


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
