*********
Changelog
*********

3.11.0
------
* Django 3.0 support
* Wagtail 2.10 support

3.10.0
------
* Wagtail 2.9 support

3.9.0
-----
* Removed 'multiselect' form field
* Wagtail 2.8 support
* Dropped Wagtail 2.0 and 2.1 support
* Integrated with GitHub actions

3.8.0
-----
* Wagtail 2.7 Support

3.7.0
-----
* Wagtail 2.6 Support

3.6.1
-----
* Republish do to pypi issue

3.6.0
-----
* Wagtail 2.5 Support

3.5.0
-----
* Wagtail 2.4 Support
* Tweak docs to ensure files work in js example (Thanks Aimee Hendrycks)

3.4.0
-----
* Support for Wagtail 2.3

3.3.0
-----
* fix issue with saving a submission with a file attached on disk.
* added new setting ``WAGTAILSTREAMFORM_ENABLE_BUILTIN_HOOKS`` default ``True`` to allow the inbuilt form processing hooks to be disabled.

3.2.0
-----
* fix template that inherited from wagtailforms to wagtailadmin

3.1.0
-----
* Support for Wagtail 2.2

3.0.0
-----
Version 3 is a major re-write and direction change and therefor any version prior
to this needs to be removed in its entirety first.

Whats New:

* Update to Wagtail 2.1
* The concept of creating a custom form class to add functionality has been removed.
* Along with the concept of custom form submission classes.
* Fields are now added via a StreamField and you can define your own like ReCAPTCHA or RegexFields.
* You can easily overwrite fields to add things like widget attributes.
* You can define a model that will allow you to save additional settings for each form.
* The form submission is processed via hooks instead of baked into the models.
* You can create as many form submission hooks as you like to process, email etc the data as you wish. These will be available to all forms that you can enable/disable at will.
* Files can now be uploaded and are stored along with the submission using the default storage.
* There is a management command to easily remove old submission data.

2.1.2
-----
* Added wagtail framework classifier

2.1.1
-----
* Fixed another migration issue

2.1.0
-----
* Update to Wagtail 2.1

2.0.1
-----
* Fixed migration issue #70

2.0.0
-----
* Added support for wagtail 2.

1.6.3
-----
* Fix issue where js was not in final package

1.6.2
-----
* Added javascript to auto populate the form slug from the name

1.6.1
-----
* Small tidy up in form code

1.6.0
-----
* Stable Release

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
