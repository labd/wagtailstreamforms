import csv
import datetime

from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from wagtail.wagtailforms.forms import SelectDateForm

from wagtailstreamforms.models import BaseForm


class SubmissionListView(SingleObjectMixin, ListView):
    paginate_by = 25
    page_kwarg = 'p'
    template_name = 'streamforms/submissions.html'
    filter_form = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=BaseForm.objects.all())
        self.filter_form = SelectDateForm(request.GET)

        if request.GET.get('action') == 'CSV':
            return self.csv()

        return super(SubmissionListView, self).get(request, *args, **kwargs)

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
        self.queryset = self.object.formsubmission_set.all()

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
        context = super(SubmissionListView, self).get_context_data(**kwargs)

        data_fields = self.object.get_data_fields()
        data_headings = [label for name, label in data_fields]

        # populate data rows from paginator
        data_rows = []
        for s in context['page_obj']:
            form_data = s.get_data()
            data_row = [form_data.get(name) for name, label in data_fields]
            data_rows.append({'model_id': s.id, 'fields': data_row})

        context['filter_form'] = self.filter_form
        context['data_rows'] = data_rows
        context['data_headings'] = data_headings

        return context
