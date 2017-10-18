from django.contrib import messages

from wagtailstreamforms.models import BaseForm


class StreamFormPageMixin(object):
    """
    A form submission mixin for a Page.

    Pages that require processing forms within their own streafields should inherit from it.
    """

    invalid_stream_form_reference = None
    invalid_stream_form = None

    def get_context(self, request, *args, **kwargs):
        """ Set the invalid form and its id in the pages context """

        context = super(StreamFormPageMixin, self).get_context(request, *args, **kwargs)

        context.update({
            'invalid_stream_form_reference': self.invalid_stream_form_reference,
            'invalid_stream_form': self.invalid_stream_form
        })

        return context

    def get_form_def(self, request):
        """ Get the form class. """

        form_id = request.POST.get('form_id')

        if form_id and form_id.isdigit():

            try:
                return BaseForm.objects.get_subclass(pk=int(form_id))
            except BaseForm.DoesNotExist:
                pass

        return None

    def serve(self, request, *args, **kwargs):
        """ If we are posting and there is a form, process it. """

        # reset these each time so we don't hang onto invalid forms on page round trips
        self.invalid_stream_form_reference = None
        self.invalid_stream_form = None

        if request.method == 'POST':

            form_def = self.get_form_def(request)

            if form_def:

                form = form_def.get_form(request.POST, request.FILES, page=self, user=request.user)

                if form.is_valid():
                    # process the form submission
                    form_def.process_form_submission(form)

                    # create success message
                    if form_def.success_message:
                        self.success_message(request, form_def)

                else:
                    # the form is invalid, set these so the FormChooserBlock
                    # can pick them up in the context
                    self.invalid_stream_form_reference = form.data.get('form_reference')
                    self.invalid_stream_form = form

        return super(StreamFormPageMixin, self).serve(request, *args, **kwargs)

    @staticmethod
    def success_message(request, form_def):
        """ Create a success message. """

        messages.success(request, form_def.success_message, fail_silently=True)
