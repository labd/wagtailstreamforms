from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup

from wagtailstreamforms.conf import settings
from wagtailstreamforms.models import BaseForm, RegexFieldValidator


class FormURLHelper(AdminURLHelper):
    def get_action_url(self, action, *args, **kwargs):
        if action == 'submissions':
            return reverse('streamforms_submissions', args=args, kwargs=kwargs)
        return super(FormURLHelper, self).get_action_url(action, *args, **kwargs)


class FormButtonHelper(ButtonHelper):
    submissions_button_classnames = []

    def submissions_button(self, pk, classnames_add=[], classnames_exclude=[]):
        classnames = self.submissions_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        button = {
            'url': self.url_helper.get_action_url('submissions', quote(pk)),
            'label': _('Submissions'),
            'classname': cn,
            'title': _('Submissions for %s') % self.verbose_name,
        }
        return button

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        btns = super(FormButtonHelper, self).get_buttons_for_obj(obj, exclude, classnames_add, classnames_exclude)
        pk = getattr(obj, self.opts.pk.attname)
        btns.append(self.submissions_button(pk, classnames_add, classnames_exclude))
        return btns


class FormModelAdmin(ModelAdmin):
    model = BaseForm
    list_display = ('name', 'latest_submission_date', 'number_of_submissions')
    menu_icon = 'icon icon-form'
    search_fields = ('name', )
    button_helper_class = FormButtonHelper
    url_helper_class = FormURLHelper

    def latest_submission_date(self, obj):
        return obj.formsubmission_set.latest('submit_time').submit_time

    def number_of_submissions(self, obj):
        return obj.formsubmission_set.count()


def _get_valid_subclasses(cls):
    clss = []
    for subcls in cls.__subclasses__():
        if subcls._meta.abstract:
            continue
        clss.append(subcls)
        sub_classes = _get_valid_subclasses(subcls)
        if sub_classes:
            clss.extend(sub_classes)
    return clss


all_classes = _get_valid_subclasses(BaseForm)
form_admins = []


# loop all subclasses of BaseForm and create model admin classes for them
for cls in all_classes:
    object_name = cls._meta.object_name
    admin_name = "{}Admin".format(object_name)
    admin_defs = {'model': cls}
    admin_class = type(admin_name, (FormModelAdmin, ), admin_defs)
    form_admins.append(admin_class)


class RegexFieldValidatorModelAdmin(ModelAdmin):
    model = RegexFieldValidator
    list_display = ('name', )
    menu_icon = 'icon icon-tick'
    search_fields = ('name', )


@modeladmin_register
class FormGroup(ModelAdminGroup):
    menu_label = _(settings.WAGTAILSTREAMFORMS_ADMIN_MENU_LABEL)
    menu_icon = 'icon icon-form'
    items = form_admins + [
        RegexFieldValidatorModelAdmin
    ]
