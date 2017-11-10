from django.conf.urls import include, url
from django.contrib import messages
from django.contrib.admin.utils import quote
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from wagtail.wagtailcore import hooks

from wagtailstreamforms.conf import get_setting
from wagtailstreamforms.models import BaseForm, RegexFieldValidator
from wagtailstreamforms.utils import get_form_instance_from_request, get_valid_subclasses


class FormURLHelper(AdminURLHelper):
    def get_action_url(self, action, *args, **kwargs):
        if action == 'copy':
            return reverse('wagtailstreamforms:streamforms_copy', args=args, kwargs=kwargs)
        elif action == 'submissions':
            return reverse('wagtailstreamforms:streamforms_submissions', args=args, kwargs=kwargs)
        return super(FormURLHelper, self).get_action_url(action, *args, **kwargs)


class FormButtonHelper(ButtonHelper):

    def copy_button(self, pk, classnames_add=[], classnames_exclude=[]):
        cn = self.finalise_classname(classnames_add, classnames_exclude)
        button = {
            'url': self.url_helper.get_action_url('copy', quote(pk)),
            'label': _('Copy'),
            'classname': cn,
            'title': _('Copy this %s') % self.verbose_name,
        }
        return button

    def submissions_button(self, pk, classnames_add=[], classnames_exclude=[]):
        cn = self.finalise_classname(classnames_add, classnames_exclude)
        button = {
            'url': self.url_helper.get_action_url('submissions', quote(pk)),
            'label': _('Submissions'),
            'classname': cn,
            'title': _('Submissions of this %s') % self.verbose_name,
        }
        return button

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        btns = super(FormButtonHelper, self).get_buttons_for_obj(obj, exclude, classnames_add, classnames_exclude)
        pk = getattr(obj, self.opts.pk.attname)
        ph = self.permission_helper
        usr = self.request.user
        btns.append(self.submissions_button(pk, classnames_add, classnames_exclude))
        if ph.user_can_create(usr):
            btns.append(self.copy_button(pk, classnames_add, classnames_exclude))
        return btns


class FormModelAdmin(ModelAdmin):
    model = BaseForm
    list_display = ('name', 'slug', 'latest_submission_date', 'number_of_submissions')
    menu_icon = 'icon icon-form'
    search_fields = ('name', 'slug')
    button_helper_class = FormButtonHelper
    url_helper_class = FormURLHelper
    form_view_extra_js = [
        static('streamforms/js/form-editor.js')
    ]

    def latest_submission_date(self, obj):
        submission_class = obj.get_submission_class()
        return submission_class._default_manager.filter(form=obj).latest('submit_time').submit_time

    def number_of_submissions(self, obj):
        submission_class = obj.get_submission_class()
        return submission_class._default_manager.filter(form=obj).count()


# loop all subclasses of BaseForm and create model admin classes for them
form_admins = []
for cls in get_valid_subclasses(BaseForm):
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


@hooks.register('register_admin_urls')
def register_admin_urls():
    from wagtailstreamforms import urls
    return [
        url(r'^wagtailstreamforms/', include((urls, 'wagtailstreamforms'))),
    ]


@modeladmin_register
class FormGroup(ModelAdminGroup):
    menu_label = _(get_setting('ADMIN_MENU_LABEL'))
    menu_order = get_setting('ADMIN_MENU_ORDER')
    menu_icon = 'icon icon-form'
    items = form_admins + [
        RegexFieldValidatorModelAdmin
    ]


@hooks.register('before_serve_page')
def process_form(page, request, *args, **kwargs):
    """ Process the form if there is one, if not just continue. """

    # only process if settings.WAGTAILSTREAMFORMS_ENABLE_FORM_PROCESSING is True
    if not get_setting('ENABLE_FORM_PROCESSING'):
        return

    if request.method == 'POST':
        form_def = get_form_instance_from_request(request)

        if form_def:
            form = form_def.get_form(request.POST, request.FILES, page=page, user=request.user)
            context = page.get_context(request, *args, **kwargs)

            if form.is_valid():
                # process the form submission
                form_def.process_form_submission(form)

                # create success message
                if form_def.success_message:
                    messages.success(request, form_def.success_message, fail_silently=True)

                # redirect to the page defined in the form
                # or the current page as a fallback - this will avoid refreshing and submitting again
                redirect_page = form_def.post_redirect_page or page

                return redirect(redirect_page.get_url(request), context=context)

            else:
                # update the context with the invalid form and serve the page
                context.update({
                    'invalid_stream_form_reference': form.data.get('form_reference'),
                    'invalid_stream_form': form
                })

                # create error message
                if form_def.error_message:
                    messages.error(request, form_def.error_message, fail_silently=True)

                return TemplateResponse(
                    request,
                    page.get_template(request, *args, **kwargs),
                    context
                )
