from django.conf.urls import include
from django.contrib import messages
from django.contrib.admin.utils import quote
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.translation import ugettext_lazy as _

from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.menus import ModelAdminMenuItem
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import CreateView, EditView
from wagtail.core import hooks

from wagtailstreamforms.conf import get_setting
from wagtailstreamforms.models import Form
from wagtailstreamforms.utils.loading import get_advanced_settings_model
from wagtailstreamforms.utils.requests import get_form_instance_from_request


SettingsModel = get_advanced_settings_model()


class FormURLHelper(AdminURLHelper):
    def get_action_url(self, action, *args, **kwargs):
        if action in ['copy', 'submissions']:
            return reverse('wagtailstreamforms:streamforms_%s' % action, args=args, kwargs=kwargs)

        return super().get_action_url(action, *args, **kwargs)


class FormButtonHelper(ButtonHelper):
    def button(self, pk, action, label, title, classnames_add, classnames_exclude):
        cn = self.finalise_classname(classnames_add, classnames_exclude)
        url = self.url_helper.get_action_url(action, quote(pk))

        button = {
            'url': url,
            'label': label,
            'classname': cn,
            'title': title,
        }

        return button

    def advanced_button(self, pk, action, label, title, classnames_add, classnames_exclude):
        cn = self.finalise_classname(classnames_add, classnames_exclude)

        try:
            advanced = SettingsModel.objects.get(form_id=pk)
            url = AdvancedSettingsModelAdmin().url_helper.get_action_url('edit', quote(advanced.pk))
        except SettingsModel.DoesNotExist:
            url = AdvancedSettingsModelAdmin().url_helper.get_action_url('create')
            url = '%s?form=%s' % (url, pk)

        button = {
            'url': url,
            'label': label,
            'classname': cn,
            'title': title,
        }

        return button

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None, classnames_exclude=None):
        buttons = super().get_buttons_for_obj(obj, exclude, classnames_add, classnames_exclude)
        pk = getattr(obj, self.opts.pk.attname)
        ph = self.permission_helper
        usr = self.request.user

        # if there is a form settings model defined
        # users that either create or edit forms should be able edit advanced settings
        if SettingsModel and (ph.user_can_create(usr) or ph.user_can_edit_obj(usr, obj)):
            buttons.append(
                self.advanced_button(
                    pk,
                    'advanced',
                    _('Advanced'),
                    _('Advanced settings'),
                    classnames_add,
                    classnames_exclude
                )
            )

        # users that can create forms can copy them
        if ph.user_can_create(usr):
            buttons.append(
                self.button(
                    pk,
                    'copy',
                    _('Copy'),
                    _('Copy this form'),
                    classnames_add,
                    classnames_exclude
                )
            )

        # users that can do any form actions can vies submissions
        buttons.append(
            self.button(
                pk,
                'submissions',
                _('Submissions'),
                _('Submissions of this form'),
                classnames_add,
                classnames_exclude
            )
        )

        return buttons


@modeladmin_register
class FormModelAdmin(ModelAdmin):
    model = Form
    list_display = ('title', 'slug', 'latest_submission', 'saved_submissions')
    menu_label = _(get_setting('ADMIN_MENU_LABEL'))
    menu_order = get_setting('ADMIN_MENU_ORDER')
    menu_icon = 'icon icon-form'
    search_fields = ('title', 'slug')
    button_helper_class = FormButtonHelper
    url_helper_class = FormURLHelper

    def latest_submission(self, obj):
        submission_class = obj.get_submission_class()
        return submission_class._default_manager.filter(form=obj).latest('submit_time').submit_time

    latest_submission.short_description = _('Latest submission')

    def saved_submissions(self, obj):
        submission_class = obj.get_submission_class()
        return submission_class._default_manager.filter(form=obj).count()

    saved_submissions.short_description = _('Saved submissions')


class AdvancedSettingsModelAdmin(ModelAdmin):

    class AdvancedCreateView(CreateView):
        def get_instance(self):
            instance = super().get_instance()
            instance.form_id = self.request.GET.get('form', None)
            return instance

        def get_success_url(self):
            return FormModelAdmin().url_helper.index_url

    class AdvancedEditView(EditView):
        def get_success_url(self):
            return FormModelAdmin().url_helper.index_url

    model = SettingsModel
    create_view_class = AdvancedCreateView
    edit_view_class = AdvancedEditView

    def get_menu_item(self, order=None):
        class AdvancedHiddenMenuItem(ModelAdminMenuItem):
            def is_shown(self, request):
                return False

        return AdvancedHiddenMenuItem(self, 999)


if SettingsModel:
    modeladmin_register(AdvancedSettingsModelAdmin)


@hooks.register('register_admin_urls')
def register_admin_urls():
    from wagtailstreamforms import urls
    return [
        path('wagtailstreamforms/', include((urls, 'wagtailstreamforms'))),
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
