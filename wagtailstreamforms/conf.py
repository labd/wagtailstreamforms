from django.conf import settings

from appconf import AppConf


class AppConf(AppConf):
    ADMIN_MENU_LABEL = 'Streamforms'
    ADMIN_MENU_ORDER = None
    ENABLE_FORM_PROCESSING = True
    FORM_TEMPLATES = (
        ('streamforms/form_block.html', 'Default Form Template'),
    )

    class Meta:
        prefix = 'wagtailstreamforms'
