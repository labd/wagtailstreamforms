from django.http import JsonResponse
from django.utils import six
from django.views.generic import View

from wagtail_streamforms.models import BaseForm


class FormSubmitView(View):
    http_method_names = ['post', ]

    def post(self, request, pk):
        try:
            form_def = BaseForm.objects.get_subclass(pk=pk)
        except BaseForm.DoesNotExist:
            err = {'message': 'error', 'detail': 'Could not find stream field form with id {}'.format(pk)}
            return JsonResponse(err, status=400)

        form = form_def.get_form(request.POST)

        if form.is_valid():
            form_def.process_form_submission(form)
        else:
            err = {'message': 'error', 'detail': form.errors}
            return JsonResponse(err, status=400)

        resp = {'message': form_def.success_message or six.text_type('success')}
        return JsonResponse(resp)
