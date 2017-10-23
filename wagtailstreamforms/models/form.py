import json
import six

from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager
from modelcluster.models import ClusterableModel
from multi_email_field.fields import MultiEmailField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, TabbedInterface, ObjectList, PageChooserPanel
from wagtailstreamforms.conf import settings
from wagtailstreamforms.forms import FormBuilder
from wagtailstreamforms.utils import recaptcha_enabled

from .submission import FormSubmission


class BaseForm(ClusterableModel):
    """ A form base class, any form should inherit from this. """

    name = models.CharField(
        max_length=255
    )
    template_name = models.CharField(
        verbose_name='template',
        max_length=255,
        choices=settings.WAGTAILSTREAMFORMS_FORM_TEMPLATES
    )
    submit_button_text = models.CharField(
        max_length=100,
        default='Submit'
    )
    store_submission = models.BooleanField(
        default=False
    )
    add_recaptcha = models.BooleanField(
        default=False,
        help_text=_('Add a reCapcha field to the form.')
    )
    success_message = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('An optional success message to show when the form has been successfully submitted')
    )
    post_redirect_page = models.ForeignKey(
        'wagtailcore.Page',
        models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text=_('The page to redirect to after a successful submission')
    )

    settings_panels = [
        FieldPanel('name', classname='full'),
        FieldPanel('template_name'),
        FieldPanel('submit_button_text'),
        FieldPanel('success_message', classname='full'),
        FieldPanel('store_submission'),
        PageChooserPanel('post_redirect_page')
    ]

    field_panels = [
        InlinePanel('form_fields', label='Fields'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(settings_panels, heading='General'),
        ObjectList(field_panels, heading='Fields'),
    ])

    objects = InheritanceManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = _('form')

    def get_data_fields(self):
        """
        Returns a list of tuples with (field_name, field_label).
        """

        data_fields = [
            ('submit_time', _('Submission date')),
        ]
        data_fields += [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]

        return data_fields

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        form_params = self.get_form_parameters()
        form_params.update(kwargs)

        return form_class(*args, **form_params)

    def get_form_class(self):
        fb = FormBuilder(self.get_form_fields(), add_recaptcha=self.add_recaptcha)
        return fb.get_form_class()

    def get_form_fields(self):
        """
        Form expects `form_fields` to be declared.
        If you want to change backwards relation name,
        you need to override this method.
        """

        return self.form_fields.all()

    def get_form_parameters(self):
        return {}

    def get_submission_class(self):
        """
        Returns submission class.

        You can override this method to provide custom submission class.
        Your class must be inherited from AbstractFormSubmission.
        """

        return FormSubmission

    def process_form_submission(self, form):
        """
        Accepts form instance with submitted data.
        Creates submission instance if self.store_submission = True.

        You can override this method if you want to have custom creation logic.
        For example, you want to additionally send an email.
        """

        if self.store_submission:
            return self.get_submission_class().objects.create(
                form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
                form=self
            )

    @cached_property
    def specific(self):
        """ Returns the specific form instance. """

        # TODO: dig to see if another query can be avoided
        try:
            return BaseForm.objects.get_subclass(pk=self.pk)
        except BaseForm.DoesNotExist:
            return self

    @cached_property
    def specific_class(self):
        """
        Return the class that this form would be if instantiated in its
        most specific form
        """

        return self.specific.__class__


if recaptcha_enabled():  # pragma: no cover
    BaseForm.field_panels.insert(0, FieldPanel('add_recaptcha'))


class BasicForm(BaseForm):
    """ A basic form. """


class EmailForm(BaseForm):
    """ A form that sends and email. """

    # do not add these fields to the email
    ignored_fields = ['recaptcha', 'form_id', 'form_reference']

    subject = models.CharField(
        max_length=255
    )
    from_address = models.EmailField()
    to_addresses = MultiEmailField()
    message = models.TextField()
    fail_silently = models.BooleanField(
        default=True
    )

    email_panels = [
        FieldPanel('subject', classname="full"),
        FieldPanel('from_address', classname="full"),
        FieldPanel('to_addresses', classname="full"),
        FieldPanel('message', classname="full"),
        FieldPanel('fail_silently'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(BaseForm.settings_panels, heading='General'),
        ObjectList(BaseForm.field_panels, heading='Fields'),
        ObjectList(email_panels, heading='Email Submission'),
    ])

    def process_form_submission(self, form):
        super(EmailForm, self).process_form_submission(form)
        self.send_form_mail(form)

    def send_form_mail(self, form):
        content = [self.message + '\n\nSubmission\n', ]

        for name, field in form.fields.items():
            data = form.cleaned_data.get(name)

            if name in self.ignored_fields or not data:
                continue  # pragma: no cover

            label = field.label or name

            content.append(label + ': ' + six.text_type(data))

        send_mail(
            self.subject,
            '\n'.join(content),
            self.from_address,
            self.to_addresses,
            self.fail_silently
        )
