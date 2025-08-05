from django.contrib import messages
from django.contrib.admin.utils import quote
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import include, path, reverse
from django.utils.translation import gettext_lazy as _
from generic_chooser.views import ModelChooserViewSet
from wagtail import hooks
from wagtail.admin import messages as wagtail_messages
from wagtail.admin.widgets import AdminPageChooser
from wagtail_modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_modeladmin.views import (
    CreateView,
    DeleteView,
    EditView,
    InspectView,
)

from wagtailstreamforms import hooks as form_hooks
from wagtailstreamforms.conf import get_setting
from wagtailstreamforms.models import Form
from wagtailstreamforms.utils.loading import get_advanced_settings_model
from wagtailstreamforms.utils.requests import get_form_instance_from_request

SettingsModel = get_advanced_settings_model()


class FormURLHelper(AdminURLHelper):
    def get_action_url(self, action, *args, **kwargs):
        if action in ["advanced", "copy", "submissions"]:
            return reverse("wagtailstreamforms:streamforms_%s" % action, args=args, kwargs=kwargs)

        return super().get_action_url(action, *args, **kwargs)


class FormButtonHelper(ButtonHelper):
    def button(self, pk, action, label, title, classnames_add, classnames_exclude):
        cn = self.finalise_classname(classnames_add, classnames_exclude)
        button = {
            "url": self.url_helper.get_action_url(action, quote(pk)),
            "label": label,
            "classname": cn,
            "title": title,
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
                self.button(
                    pk,
                    "advanced",
                    _("Advanced"),
                    _("Advanced settings"),
                    classnames_add,
                    classnames_exclude,
                )
            )

        # users that can create forms can copy them
        if ph.user_can_create(usr):
            buttons.append(
                self.button(
                    pk,
                    "copy",
                    _("Copy"),
                    _("Copy this form"),
                    classnames_add,
                    classnames_exclude,
                )
            )

        # users that can do any form actions can view submissions
        buttons.append(
            self.button(
                pk,
                "submissions",
                _("Submissions"),
                _("Submissions of this form"),
                classnames_add,
                classnames_exclude,
            )
        )

        return buttons


class InstanceSpecificViewHookMixin:
    """Mixin class responsible to apply wagtailstreamforms specific hooks."""

    def dispatch(self, request, *args, **kwargs):
        for fn in form_hooks.get_hooks("before_inspect_form_instance_dispatch"):
            self.instance = fn(self.instance, request)
        return super().dispatch(request, *args, **kwargs)


class InspectFormView(InstanceSpecificViewHookMixin, InspectView):
    pass


class CreateFormView(CreateView):
    def form_valid(self, form):
        instance = form.save(commit=False)
        for fn in form_hooks.get_hooks("before_form_save"):
            instance = fn(instance, self.request)
        instance.save()
        wagtail_messages.success(
            self.request,
            self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance),
        )
        return redirect(self.get_success_url())


class EditFormView(InstanceSpecificViewHookMixin, EditView):
    pass


class DeleteFormView(InstanceSpecificViewHookMixin, DeleteView):
    pass


@modeladmin_register
class FormModelAdmin(ModelAdmin):
    model = Form
    list_display = ("title", "slug", "latest_submission", "saved_submissions")
    list_filter = None
    menu_label = _(get_setting("ADMIN_MENU_LABEL"))
    menu_order = get_setting("ADMIN_MENU_ORDER")
    menu_icon = "form"
    search_fields = ("title", "slug")
    button_helper_class = FormButtonHelper
    inspect_view_class = InspectFormView
    create_view_class = CreateFormView
    edit_view_class = EditFormView
    delete_view_class = DeleteFormView
    url_helper_class = FormURLHelper
    index_template_name = "modeladmin/index.html"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        for fn in form_hooks.get_hooks("construct_form_queryset"):
            qs = fn(qs, request)
        return qs

    def get_list_display(self, request):
        list_display = self.list_display
        for fn in form_hooks.get_hooks("construct_form_list_display"):
            list_display = fn(list_display, request)
        return list_display

    def get_list_filter(self, request):
        list_filter = self.list_filter
        for fn in form_hooks.get_hooks("construct_form_list_filter"):
            list_filter = fn(list_filter, request)
        return list_filter

    def latest_submission(self, obj):
        submission_class = obj.get_submission_class()
        return submission_class._default_manager.filter(form=obj).latest("submit_time").submit_time

    latest_submission.short_description = _("Latest submission")

    def saved_submissions(self, obj):
        submission_class = obj.get_submission_class()
        return submission_class._default_manager.filter(form=obj).count()

    saved_submissions.short_description = _("Saved submissions")


@hooks.register("register_admin_urls")
def register_admin_urls():
    from wagtailstreamforms import urls

    return [path("wagtailstreamforms/", include((urls, "wagtailstreamforms")))]


@hooks.register("before_serve_page")
def process_form(page, request, *args, **kwargs):
    """Process the form if there is one, if not just continue."""

    # only process if settings.WAGTAILSTREAMFORMS_ENABLE_FORM_PROCESSING is True
    if not get_setting("ENABLE_FORM_PROCESSING"):
        return

    if request.method == "POST":
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
                # or the current page as a fallback - this will avoid refreshing
                # and submitting again
                redirect_page = form_def.post_redirect_page or page

                return redirect(redirect_page.get_url(request), context=context)

            else:
                # update the context with the invalid form and serve the page
                context.update(
                    {
                        "invalid_stream_form_reference": form.data.get("form_reference"),
                        "invalid_stream_form": form,
                    }
                )

                # create error message
                if form_def.error_message:
                    messages.error(request, form_def.error_message, fail_silently=True)

                return TemplateResponse(
                    request, page.get_template(request, *args, **kwargs), context
                )


class WagtailStreamFormsChooserViewSet(ModelChooserViewSet):
    icon = "form"
    model = Form
    page_title = _("Choose a form")
    per_page = 10


class WagtailStreamFormsChooser(AdminPageChooser):
    choose_one_text = _("Choose a form")
    choose_another_text = _("Choose another form")
    link_to_chosen_text = _("Edit this form")
    model = Form
    choose_modal_url_name = "wagtailstreamforms_chooser:choose"
    icon = "form"


@hooks.register("register_admin_viewset")
def register_wagtailstreamforms_chooser_viewset():
    return WagtailStreamFormsChooserViewSet(
        "wagtailstreamforms_chooser", url_prefix="wagtailstreamforms-chooser"
    )
