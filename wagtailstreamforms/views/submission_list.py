import csv
import datetime

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.contrib.forms.forms import SelectDateForm
from wagtailstreamforms.models import BaseForm


class SubmissionListView(SingleObjectMixin, ListView):
    paginate_by = 25
    page_kwarg = 'p'
    template_name = 'streamforms/submissions.html'
    filter_form = None
    model = BaseForm

    @property
    def permission_helper(self):
        return PermissionHelper(model=self.object.specific_class)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.permission_helper.user_can_list(self.request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            return self.model.objects.get(pk=pk).specific
        except self.model.DoesNotExist:
            raise Http404(_("No BaseForm found matching the query"))

    def get(self, request, *args, **kwargs):
        self.filter_form = SelectDateForm(request.GET)

        if request.GET.get('action') == 'CSV':
            return self.csv()

        return super().get(request, *args, **kwargs)

    def csv(self):
        queryset = self.get_queryset()
        data_fields = self.object.get_data_fields()
        data_headings = [smart_str(label) for name, label in data_fields]

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment;filename=export.csv'

        writer = csv.writer(response)
        writer.writerow(data_headings)
        for s in queryset:
            data_row = []
            form_data = s.get_data()
            for name, label in data_fields:
                data_row.append(smart_str(form_data.get(name)))
            writer.writerow(data_row)

        return response

    def get_queryset(self):
        submission_class = self.object.get_submission_class()
        self.queryset = submission_class._default_manager.filter(form=self.object)

        # filter the queryset by the required dates
        if self.filter_form.is_valid():
            date_from = self.filter_form.cleaned_data.get('date_from')
            date_to = self.filter_form.cleaned_data.get('date_to')
            if date_from:
                self.queryset = self.queryset.filter(submit_time__gte=date_from)
            if date_to:
                date_to += datetime.timedelta(days=1)
                self.queryset = self.queryset.filter(submit_time__lte=date_to)

        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data_fields = self.object.get_data_fields()
        data_headings = [label for name, label in data_fields]

        # populate data rows from paginator
        data_rows = []
        for s in context['page_obj']:
            form_data = s.get_data()
            data_row = [form_data.get(name) for name, label in data_fields]
            data_rows.append({'model_id': s.id, 'fields': data_row})

        context.update({
            'filter_form': self.filter_form,
            'data_rows': data_rows,
            'data_headings': data_headings,
            'has_delete_permission': self.permission_helper.user_can_delete_obj(self.request.user, self.object)
        })

        return context
