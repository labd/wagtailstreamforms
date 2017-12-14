from django.conf.urls import url

from wagtailstreamforms.views import (
    CopyFormView,
    SubmissionDeleteView,
    SubmissionListView
)


urlpatterns = [
    url(r'^(?P<pk>\d+)/copy/$', CopyFormView.as_view(), name='streamforms_copy'),
    url(r'^(?P<pk>\d+)/submissions/$', SubmissionListView.as_view(), name='streamforms_submissions'),
    url(r'^(?P<pk>\d+)/submissions/delete/$', SubmissionDeleteView.as_view(), name='streamforms_delete_submissions'),
]
