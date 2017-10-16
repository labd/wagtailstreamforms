Form Customisation
==================

Currently we have defined two different types of forms, one which just
enables saving the submission and one to additionally email the results of
the submission.

You can easily add your own all you have to do is create a model that
inherits from ``wagtailstreamforms.models.BaseForm`` add any additional fields or properties and
this will be added to the cms admin area.

Example:

::

    from wagtailstreamforms.models import BaseForm

    class SomeForm(BaseForm):

        def process_form_submission(self, form):
            super(SomeForm, self).process_form_submission(form) # handles the submission saving
            # do your own stuff here

Reference
---------

.. autoclass:: wagtailstreamforms.models.BaseForm
   :members:

.. autoclass:: wagtailstreamforms.models.BasicForm
   :members:

.. autoclass:: wagtailstreamforms.models.EmailForm
   :members:

.. autoclass:: wagtailstreamforms.models.AbstractFormSubmission
   :members:

.. autoclass:: wagtailstreamforms.models.FormSubmission
   :members: