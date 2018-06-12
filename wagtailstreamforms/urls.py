from django.urls import path

from wagtailstreamforms import views


urlpatterns = [
    path('<int:pk>/advanced/', views.AdvancedSettingsView.as_view(), name='streamforms_advanced'),
    path('<int:pk>/copy/', views.CopyFormView.as_view(), name='streamforms_copy'),
    path('<int:pk>/submissions/', views.SubmissionListView.as_view(), name='streamforms_submissions'),
    path('<int:pk>/submissions/delete/', views.SubmissionDeleteView.as_view(), name='streamforms_delete_submissions'),
]
