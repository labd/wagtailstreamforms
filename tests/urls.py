from django.conf.urls import url, include

from wagtail_streamforms import urls as streamforms_urls


urlpatterns = [
    url(r'^forms/', include(streamforms_urls)),
]