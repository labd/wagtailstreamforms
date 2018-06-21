Fields
======

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
- singlefile
- multifile

The various default options for the fields are set when choosing that type of field within the StreamField.
For example a dropdown includes options to set the ``choices`` and an additional ``empty_label`` as the
first choice.

Adding new fields
-----------------

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
        # the form field class
        field_class = forms.CharField
        # the widget for the form field
        widget = forms.widgets.Textarea
        # the icon in the streamfield
        icon = 'placeholder'
        # the label to show in the streamfield
        label = 'My text area'

Setting widget attributes
-------------------------

Setting widget attributes can be done on the ``BaseField`` class as follows:

.. code-block:: python

    @register('mytextarea')
    class CustomTextAreaField(BaseField):
        field_class = forms.CharField
        widget = forms.widgets.Textarea(attrs={'rows': 10})

Setting field options
---------------------

The ``BaseField`` class has a default dict of options set from the StreamField's StructValue:

.. code-block:: python

    class BaseField:
        def get_options(self, block_value):
            return {
                'label': block_value.get('label'),
                'help_text': block_value.get('help_text'),
                'required': block_value.get('required'),
                'initial': block_value.get('default_value')
            }

You can use this to provide additional options set either by passing them from the StreamField
or manually setting them. The below adds django's slug validator to create a slug field:

.. code-block:: python

    from django.core import validators

    @register('slug')
    class SlugField(BaseField):
        field_class = forms.CharField

        def get_options(self, block_value):
            options = super().get_options(block_value)
            options.update({'validators': [validators.validate_slug]})
            return options

Editable field options
----------------------

To be able to make the field options editable from within the StreamField you must override
the ``BaseField.get_form_block()`` method with the additonal options you will require.

Consider that you need a max length on a ``CharField`` but want the length to be configurable
on every instance of that field. Firstly you need to setup the field's StructBlock so that the
additional options are available within the StreamField:

.. code-block:: python

    @register('maxlength')
    class MaxLengthField(BaseField):
        field_class = forms.CharField
        label = 'Text field (max length)'

        def get_form_block(self):
            return blocks.StructBlock([
                ('label', blocks.CharBlock()),
                ('help_text', blocks.CharBlock(required=False)),
                ('required', blocks.BooleanBlock(required=False)),
                ('max_length', blocks.IntegerBlock(required=True)),
                ('default_value', blocks.CharBlock(required=False)),
            ], icon=self.icon, label=self.label)

and then pull that value into the fields options:


.. code-block:: python

    @register('maxlength')
    class MaxLengthField(BaseField):
        field_class = forms.CharField
        label = 'Text field (max length)'

        def get_options(self, block_value):
            options = super().get_options(block_value)
            options.update({'max_length': block_value.get('max_length')})
            return options

        def get_form_block(self):
            return blocks.StructBlock([
                ('label', blocks.CharBlock()),
                ('help_text', blocks.CharBlock(required=False)),
                ('required', blocks.BooleanBlock(required=False)),
                ('max_length', blocks.IntegerBlock(required=True)),
                ('default_value', blocks.CharBlock(required=False)),
            ], icon=self.icon, label=self.label)

Overriding an existing field
----------------------------

.. important::
   When overriding an existing field make sure the app that has the ``wagtailstreamforms_fields.py``
   file appears after ``wagtailstreamforms`` in your ``INSTALLED_APPS`` or the field will not be overridden.

You can replace one of the form fields by simply using an existing name in the ``@register`` decorator.
Suppose you want to add a rows attribute to the textarea widget of the ``multiline`` field.

In your ``wagtailstreamforms_fields.py`` file:

.. code-block:: python

    @register('multiline')
    class MultiLineTextField(BaseField):
        field_class = forms.CharField
        widget = forms.widgets.Textarea(attrs={'rows': 10})

Using file fields
-----------------

To handle file fields correctly you must ensure the your form template has the correct enctype.
you can automatically add this with a simple if statement to detect if the form is a multipart type form.

.. code-block:: html

   <form{% if form.is_multipart %} enctype="multipart/form-data"{% endif %} action="...

Files will be uploaded using your default storage class to the path ``streamforms/`` and are listed
along with the form submissions. When a submission is deleted all files are also deleted from the storage.

Examples
--------

Below are some examples of useful fields.

Model choice
^^^^^^^^^^^^

An example model choice field of users.

.. code-block:: python

   from django import forms
   from django.contrib.auth.models import User

   from wagtail.core import blocks
   from wagtailstreamforms.fields import BaseField, register


   @register('user')
   class UserChoiceField(BaseField):
       field_class = forms.ModelChoiceField
       icon = 'arrow-down-big'
       label = 'User dropdown field'

       @staticmethod
       def get_queryset():
           return User.objects.all()

       def get_options(self, block_value):
           options = super().get_options(block_value)
           options.update({'queryset': self.get_queryset()})
           return options

       def get_form_block(self):
           return blocks.StructBlock([
               ('label', blocks.CharBlock()),
               ('help_text', blocks.CharBlock(required=False)),
               ('required', blocks.BooleanBlock(required=False)),
           ], icon=self.icon, label=self.label)

Regex validated
^^^^^^^^^^^^^^^

An example field that allows a selection of regex patterns with an option to set the invalid error message.

Taking this further you could provide the invalid error messages from code if they were always
the same for any given regex pattern.

.. code-block:: python

   from django import forms

   from wagtail.core import blocks
   from wagtailstreamforms.fields import BaseField, register

   @register('regex_validated')
   class RegexValidatedField(BaseField):
       field_class = forms.RegexField
       label = 'Regex field'

       def get_options(self, block_value):
           options = super().get_options(block_value)
           options.update({
               'regex': block_value.get('regex'),
               'error_messages': {'invalid': block_value.get('error_message')}
           })
           return options

       def get_regex_choices(self):
           return (
               ('(.*?)', 'Any'),
               ('^[a-zA-Z0-9]+$', 'Letters and numbers only'),
           )

       def get_form_block(self):
           return blocks.StructBlock([
               ('label', blocks.CharBlock()),
               ('help_text', blocks.CharBlock(required=False)),
               ('required', blocks.BooleanBlock(required=False)),
               ('regex', blocks.ChoiceBlock(choices=self.get_regex_choices())),
               ('error_message', blocks.CharBlock()),
               ('default_value', blocks.CharBlock(required=False)),
           ], icon=self.icon, label=self.label)

ReCAPTCHA
^^^^^^^^^

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
    # enable no captcha
    NOCAPTCHA = True


``wagtailstreamforms_fields.py`` file:

.. code-block:: python

    from captcha.fields import ReCaptchaField
    from wagtail.core import blocks
    from wagtailstreamforms.fields import BaseField, register

    @register('recaptcha')
    class ReCaptchaField(BaseField):
        field_class = ReCaptchaField
        icon = 'success'
        label = 'ReCAPTCHA field'

        def get_options(self, block_value):
             options = super().get_options(block_value)
             options.update({
                 'required': True
             })
             return options

        def get_form_block(self):
            return blocks.StructBlock([
                ('label', blocks.CharBlock()),
                ('help_text', blocks.CharBlock(required=False)),
            ], icon=self.icon, label=self.label)

Useful Resources
----------------

* `Django Documentation - Form fields <https://docs.djangoproject.com/en/2.1/ref/forms/fields/>`_

Reference
---------

.. autoclass:: wagtailstreamforms.fields.BaseField
   :members:
