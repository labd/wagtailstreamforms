from django.test import override_settings

from wagtailstreamforms.urls import urlpatterns

from .test_case import AppTestCase


class UrlsTests(AppTestCase):
    @override_settings(WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL=None)
    def test_no_advanced_url_when_no_setting(self):
        self.reload_module("wagtailstreamforms.urls")
        self.assertEqual(len(urlpatterns), 4)

    @override_settings(WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL="tests.ValidFormSettingsModel")
    def test_advanced_url_when_setting_exists(self):
        self.reload_module("wagtailstreamforms.urls")
        self.assertEqual(len(urlpatterns), 4)
