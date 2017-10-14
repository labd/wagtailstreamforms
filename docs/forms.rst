Writing your own form functionality
===================================

Currently we have defined two different types of forms, one which just
enables saving the submission and one to addionally email the results of
the submission.

You can easily add your own all you have to do is create a model that
inherits from ``wagtailstreamforms.models.BaseForm`` add any addional fields or properties and
this will be added to the cms admin area.

Example:

::

    from wagtailstreamforms.models import BaseForm

    class SomeForm(BaseForm):

        def process_form_submission(self, form):
            super(SomeForm, self).process_form_submission(form) # handles the submission saving
            # do your own stuff here
