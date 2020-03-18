from django.conf.urls import include, url
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^cms/", include(wagtailadmin_urls)),
    url(r"", include(wagtail_urls)),
]
