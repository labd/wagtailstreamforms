from django.conf.urls import url, include

from wagtail.wagtailadmin import urls as wagtailadmin_urls

from wagtail_streamforms import urls as streamforms_urls


urlpatterns = [
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^forms/', include(streamforms_urls)),
]