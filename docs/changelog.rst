Changelog
=========

Whats next
----------

*

1.5.2
-----

* Added ``AbstractEmailForm`` to more easily allow creating additional form types.

1.5.1
-----

* Fix migrations being regenerated when template choices change

1.5.0
-----

* Removed all project dependencies except wagtail and recapcha
* The urls no longer need to be specified in your ``urls.py`` and can be removed.

1.4.4
-----

* The template tag now has the full page context incase u need a reference to the user or page

1.4.3
-----

* Fixed bug where messages are not available in the template tags context

1.4.2
-----

* Removed label value from recapcha field
* Added setting to set order of menu item in cms admin

1.4.1
-----

* Added an optional error message to display if the forms have errors

1.4.0
-----

* Added a template tag that can be used to render a form. Incase you want it to appear outside a streamfield

1.3.0
-----

* A form and it's fields can easily be copied to a new form from within the admin area

1.2.3
-----

* Fix paginator on submission list not remembering date filters

1.2.2
-----

* Form submission viewing and deleting permissions have been implemented

1.2.1
-----

* On the event that a form is deleted that is still referenced in a streamfield, we are rendering a generic template that can be overridden to warn the end user

1.2.0
-----

* In the form builder you can now specify a page to redirect to upon successful submission of the form
* The page mixin StreamFormPageMixin that needed to be included in every page has now been replaced by a wagtail before_serve_page hook so you will need to remove this mixin

1.1.1
-----

* Fixed bug where multiple forms of same type in a streamfield were both showing validation errors when one submitted