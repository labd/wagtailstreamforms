from django.contrib import admin
from django.urls import include, re_path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^cms/", include(wagtailadmin_urls)),
    re_path(r"", include(wagtail_urls)),
]
