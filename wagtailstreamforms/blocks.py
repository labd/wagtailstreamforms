import uuid

from django.utils.functional import cached_property
from django.utils.safestring import SafeText, mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail import blocks


class InfoBlock(blocks.CharBlock):
    def render_form(self, value, prefix="", errors=None) -> SafeText:
        field = self.field
        shown_value = value if value else field.help_text
        return mark_safe('<div style="margin-top:5px;padding:0.9em 1.2em;">%s</div>' % shown_value)


class FormChooserBlock(blocks.ChooserBlock):
    @cached_property
    def target_model(self):
        from .models import Form

        return Form

    @cached_property
    def widget(self):
        from .wagtail_hooks import WagtailStreamFormsChooser

        return WagtailStreamFormsChooser()

    def get_form_state(self, value: dict):
        return self.widget.get_value_data(value)


class WagtailFormBlock(blocks.StructBlock):
    form = FormChooserBlock()
    form_action = blocks.CharBlock(
        required=False,
        help_text=_('The form post action. "" or "." for the current page or a url'),
    )
    form_reference = InfoBlock(
        required=False,
        help_text=_("This form will be given a unique reference once saved"),
    )

    class Meta:
        icon = "form"
        template = None

    def render(self, value: dict, context: dict | None = None) -> str | SafeText:
        form = value.get("form")

        # check if we have a form, as they can be deleted, and we dont want to break the site with
        # a none template value
        if form:
            self.meta.template = form.template_name
        else:
            self.meta.template = "streamforms/non_existent_form.html"

        return super().render(value, context)

    def get_context(self, value: dict, parent_context: dict | None = None) -> dict:
        context = super().get_context(value, parent_context)

        form = value.get("form")
        form_reference = value.get("form_reference")

        if form:
            # check the context for an invalid form submitted to the page.
            # Use that instead if it has the same unique form_reference number
            invalid_form_reference = context.get("invalid_stream_form_reference")
            invalid_form = context.get("invalid_stream_form")

            if (
                invalid_form_reference
                and invalid_form
                and invalid_form_reference == form_reference
            ):
                context["form"] = invalid_form
            else:
                context["form"] = form.get_form(
                    initial={"form_id": form.id, "form_reference": form_reference}
                )

        return context

    def clean(self, value: dict) -> dict:
        result = super().clean(value)

        # set to a new uuid so we can ensure we can identify this form
        # against other forms of the same type in the page
        if not result.get("form_reference"):
            result["form_reference"] = uuid.uuid4()

        return result
