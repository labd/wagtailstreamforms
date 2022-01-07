from django.urls import path

from wagtailstreamforms import views
from wagtailstreamforms.utils.loading import get_advanced_settings_model

SettingsModel = get_advanced_settings_model()


urlpatterns = [
    path("<int:pk>/copy/", views.CopyFormView.as_view(), name="streamforms_copy"),
    path(
        "<int:pk>/submissions/",
        views.SubmissionListView.as_view(),
        name="streamforms_submissions",
    ),
    path(
        "<int:pk>/submissions/delete/",
        views.SubmissionDeleteView.as_view(),
        name="streamforms_delete_submissions",
    ),
]


if SettingsModel:  # pragma: no cover
    urlpatterns += [
        path(
            "<int:pk>/advanced/",
            views.AdvancedSettingsView.as_view(),
            name="streamforms_advanced",
        )
    ]
