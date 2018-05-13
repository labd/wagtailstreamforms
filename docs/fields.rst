Form Fields
===========

Form fields are added to the form by the means of a StreamField.
There are various default fields already defined as listed below:

- singleline
- multiline
- date
- datetime
- email
- url
- number
- dropdown
- multiselect
- radio
- checkboxes
- checkbox
- hidden

The various default options for the fields are set when choosing that type of field within the StreamField.
For example a dropdown includes options to set the ``choices`` and an additional ``empty_label`` as the
first choice.

Adding fields
-------------

You can also register your own fields which will be added to the form builders StreamField.
First you need to create the file ``wagtailstreamforms_fields.py`` in the root of an app in your project
and add the following as an example:

.. code-block:: python

    from django import forms
    from wagtailstreamforms.fields import BaseField, register

    @register('mytext')
    class CustomTextField(BaseField):
        field_class = forms.CharField

This will add a simple single line charfield to the list of available fields with the type ``mytext``.

The ``BaseField`` class also has some additional properties you can set as follows:

.. code-block:: python

    @register('mytextarea')
    class CustomTextAreaField(BaseField):
        # the form field field class
        field_class = forms.CharField
        # the widget for the form field
        widget = forms.widgets.Textarea
        # the icon in the streamfield
        icon = 'placeholder'

Setting widget attributes
-------------------------

Setting widget attributes can be done on the ``BaseField`` class as follows:

.. code-block:: python

   from django import forms
   from wagtailstreamforms.fields import BaseField, register

   @register('mytextarea')
   class CustomTextAreaField(BaseField):
      field_class = forms.CharField
      widget = forms.widgets.Textarea(attrs={'rows': 10})

Overriding an existing field
----------------------------

.. important::
   When overriding an existing field make sure the app that has the ``wagtailstreamforms_fields.py``
   file appears after ``wagtailstreamforms`` in your ``INSTALLED_APPS`` or the field will not be overridden.

You can replace one of the form fields by simply using an existing name in the ``@register`` decorator.
Suppose you want to add a rows attribute to the textarea widget of the ``multiline`` field.

In your ``wagtailstreamforms_fields.py`` file:

.. code-block:: python

   from django import forms
   from wagtailstreamforms.fields import BaseField, register

   @register('multiline')
   class MultiLineTextField(BaseField):
      field_class = forms.CharField
      widget = forms.widgets.Textarea(attrs={'rows': 10})

ReCAPTCHA example
-----------------

Adding a ReCAPTCHA field is as simple as follows.

Installing ``django-recaptcha``:

.. code-block:: python

   pip install django-recaptcha

Django ``settings.py`` file:

.. code-block:: python

   INSTALLED_APPS = [
       ...
       'captcha'
       ...
   ]

   # developer keys
   RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
   RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
   NOCAPTCHA = True


``wagtailstreamforms_fields.py`` file:

.. code-block:: python

   from captcha.fields import ReCaptchaField
   from wagtailstreamforms.fields import BaseField, register

   @register('recaptcha')
   class ReCaptchaField(BaseField):
       field_class = ReCaptchaField
       icon = 'success'

       def get_form_block(self):
           return blocks.StructBlock([
               ('label', blocks.CharBlock()),
               ('help_text', blocks.CharBlock(required=False)),
           ], icon=self.icon)

Reference
---------

.. autoclass:: wagtailstreamforms.fields.BaseField
   :members: