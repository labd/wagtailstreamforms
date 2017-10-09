from django.conf import settings

from appconf import AppConf


class AppConf(AppConf):
    FORM_TEMPLATES = (
        ('streamforms/form_block.html', 'Default Form Template'),
    )

    class Meta:
        prefix = 'wagtail_streamforms'
