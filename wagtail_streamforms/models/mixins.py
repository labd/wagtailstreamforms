from django.contrib import messages

from wagtail_streamforms.models import BaseForm


class StreamFormPageMixin(object):

    _invalid_stream_form_id = None
    _invalid_stream_form = None

    def get_context(self, request, *args, **kwargs):
        context = super(StreamFormPageMixin, self).get_context(request, *args, **kwargs)
        if self._invalid_stream_form_id:
            context.update({
                'invalid_stream_form_id': self._invalid_stream_form_id,
                'invalid_stream_form': self._invalid_stream_form
            })
        return context

    def serve(self, request, *args, **kwargs):

        # reset these each time so we don't hang onto invalid forms on page round trips
        self._invalid_stream_form_id = None
        self._invalid_stream_form = None

        if request.method == 'POST':

            # get the form id
            form_id = request.POST.get('form_id')

            # process request
            if form_id and form_id.isdigit():

                form_id = int(form_id)

                try:
                    form_def = BaseForm.objects.get_subclass(pk=form_id)
                except BaseForm.DoesNotExist:
                    form_def = None

                if form_def:

                    form = form_def.get_form(request.POST)

                    # check the form and either process it or push it back as invalid
                    if form.is_valid():
                        form_def.process_form_submission(form)

                        if form_def.success_message:
                            self.success_message(request, form_def)

                    else:
                        self._invalid_stream_form_id = form_id
                        self._invalid_stream_form = form

        return super(StreamFormPageMixin, self).serve(request, *args, **kwargs)

    @staticmethod
    def success_message(request, form_def):
        messages.success(request, form_def.success_message)
