from django.conf import settings

from appconf import AppConf


class AppConf(AppConf):
    ADMIN_MENU_LABEL = 'Streamforms'
    FORM_TEMPLATES = (
        ('streamforms/form_block.html', 'Default Form Template'),
    )

    class Meta:
        prefix = 'wagtailstreamforms'
