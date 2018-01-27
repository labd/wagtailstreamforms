from collections import defaultdict
import json
import six
import uuid

from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from modelcluster.models import ClusterableModel, get_all_child_relations
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    TabbedInterface,
    ObjectList,
    PageChooserPanel,
    MultiFieldPanel
)
from wagtailstreamforms.conf import get_setting
from wagtailstreamforms.fields import MultiEmailField
from wagtailstreamforms.forms import FormBuilder
from wagtailstreamforms.utils import recaptcha_enabled

from .submission import FormSubmission


def get_default_form_content_type():
    """
    Returns the content type to use as a default for forms whose content type
    has been deleted.
    """

    return ContentType.objects.get_for_model(BaseForm)


class BaseForm(ClusterableModel):
    """ A form base class, any form should inherit from this. """

    name = models.CharField(
        _('Name'),
        max_length=255
    )
    slug = models.SlugField(
        _('Slug'),
        allow_unicode=True,
        max_length=255,
        unique=True,
        help_text=_('Used to identify the form in template tags')
    )
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        verbose_name=_('Content type'),
        related_name='streamforms',
        on_delete=models.SET(get_default_form_content_type)
    )
    template_name = models.CharField(
        _('Template'),
        max_length=255,
        choices=get_setting('FORM_TEMPLATES')
    )
    submit_button_text = models.CharField(
        _('Submit button text'),
        max_length=100,
        default='Submit'
    )
    store_submission = models.BooleanField(
        _('Store submission'),
        default=False
    )
    add_recaptcha = models.BooleanField(
        _('Add recaptcha'),
        default=False,
        help_text=_('Add a reCapcha field to the form.')
    )
    success_message = models.CharField(
        _('Success message'),
        blank=True,
        max_length=255,
        help_text=_('An optional success message to show when the form has been successfully submitted')
    )
    error_message = models.CharField(
        _('Error message'),
        blank=True,
        max_length=255,
        help_text=_('An optional error message to show when the form has validation errors')
    )
    post_redirect_page = models.ForeignKey(
        'wagtailcore.Page',
        verbose_name=_('Post redirect page'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text=_('The page to redirect to after a successful submission')
    )

    settings_panels = [
        FieldPanel('name', classname='full'),
        FieldPanel('slug'),
        FieldPanel('template_name'),
        FieldPanel('submit_button_text'),
        MultiFieldPanel([
            FieldPanel('success_message'),
            FieldPanel('error_message'),
        ], _('Messages')),
        FieldPanel('store_submission'),
        PageChooserPanel('post_redirect_page')
    ]

    field_panels = [
        InlinePanel('form_fields', label=_('Fields')),
    ]

    edit_handler = TabbedInterface([
        ObjectList(settings_panels, heading=_('General')),
        ObjectList(field_panels, heading=_('Fields')),
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.id:
            self.content_type = ContentType.objects.get_for_model(self)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')

    def copy(self):
        """ Copy this form and its fields. """

        exclude_fields = ['id', 'slug']
        specific_self = self.specific
        specific_dict = {}

        for field in specific_self._meta.get_fields():

            # ignore explicitly excluded fields
            if field.name in exclude_fields:
                continue  # pragma: no cover

            # ignore reverse relations
            if field.auto_created:
                continue  # pragma: no cover

            # ignore m2m relations - they will be copied as child objects
            # if modelcluster supports them at all (as it does for tags)
            if field.many_to_many:
                continue  # pragma: no cover

            # ignore parent links (baseform_ptr)
            if isinstance(field, models.OneToOneField) and field.rel.parent_link:
                continue  # pragma: no cover

            specific_dict[field.name] = getattr(specific_self, field.name)

        # new instance from prepared dict values, in case the instance class implements multiple levels inheritance
        form_copy = self.specific_class(**specific_dict)

        # a dict that maps child objects to their new ids
        # used to remap child object ids in revisions
        child_object_id_map = defaultdict(dict)

        # create the slug - temp as will be changed from the copy form
        form_copy.slug = uuid.uuid4()

        form_copy.save()

        # copy child objects
        for child_relation in get_all_child_relations(specific_self):
            accessor_name = child_relation.get_accessor_name()
            parental_key_name = child_relation.field.attname
            child_objects = getattr(specific_self, accessor_name, None)

            if child_objects:
                for child_object in child_objects.all():
                    old_pk = child_object.pk
                    child_object.pk = None
                    setattr(child_object, parental_key_name, form_copy.id)
                    child_object.save()

                    # add mapping to new primary key (so we can apply this change to revisions)
                    child_object_id_map[accessor_name][old_pk] = child_object.pk

            else:  # we should never get here as there is always a FormField child class
                pass  # pragma: no cover

        return form_copy

    copy.alters_data = True

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
        """
        Return this form in its most specific subclassed form.
        """

        # the ContentType.objects manager keeps a cache, so this should potentially
        # avoid a database lookup over doing self.content_type. I think.
        content_type = ContentType.objects.get_for_id(self.content_type_id)
        model_class = content_type.model_class()
        if model_class is None:
            # Cannot locate a model class for this content type. This might happen
            # if the codebase and database are out of sync (e.g. the model exists
            # on a different git branch and we haven't rolled back migrations before
            # switching branches); if so, the best we can do is return the form
            # unchanged.
            return self  # pragma: no cover
        elif isinstance(self, model_class):
            # self is already the an instance of the most specific class
            return self
        else:
            return content_type.get_object_for_this_type(id=self.id)

    @cached_property
    def specific_class(self):
        """
        Return the class that this page would be if instantiated in its
        most specific form
        """

        content_type = ContentType.objects.get_for_id(self.content_type_id)
        return content_type.model_class()


if recaptcha_enabled():  # pragma: no cover
    BaseForm.field_panels.insert(0, FieldPanel('add_recaptcha'))


class BasicForm(BaseForm):
    """ A basic form. """
    class Meta:
        verbose_name = _('Basic form')
        verbose_name_plural = _('Basic Forms')


class AbstractEmailForm(BaseForm):
    """
    A form that sends and email.

    You can create custom form model based on this abstract model.
    For example, if you need a form that will send an email.
    """

    # do not add these fields to the email
    ignored_fields = ['recaptcha', 'form_id', 'form_reference']

    subject = models.CharField(
        _('Subject'),
        max_length=255
    )
    from_address = models.EmailField(
        _('From address')
    )
    to_addresses = MultiEmailField(
        _('To addresses'),
        help_text=_("Add one email per line")
    )
    message = models.TextField(
        _('Message'),
    )
    fail_silently = models.BooleanField(
        _('Fail silently'),
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
        ObjectList(BaseForm.settings_panels, heading=_('General')),
        ObjectList(BaseForm.field_panels, heading=_('Fields')),
        ObjectList(email_panels, heading=_('Email Submission')),
    ])

    class Meta(BaseForm.Meta):
        abstract = True

    def process_form_submission(self, form):
        """ Process the form submission and send an email. """

        super().process_form_submission(form)
        self.send_form_mail(form)

    def send_form_mail(self, form):
        """ Send an email. """

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


class EmailForm(AbstractEmailForm):
    """ A form that sends and email. """
    class Meta:
        verbose_name = _('Email form')
        verbose_name_plural = _('Email forms')
