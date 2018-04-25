from django.urls import path

from wagtailstreamforms.views import (
    CopyFormView,
    SubmissionDeleteView,
    SubmissionListView
)


urlpatterns = [
    path('<int:pk>/copy/', CopyFormView.as_view(), name='streamforms_copy'),
    path('<int:pk>/submissions/', SubmissionListView.as_view(), name='streamforms_submissions'),
    path('<int:pk>/submissions/delete/', SubmissionDeleteView.as_view(), name='streamforms_delete_submissions'),
]
