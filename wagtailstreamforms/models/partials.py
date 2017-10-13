import six

from django.core.mail import send_mail
from django.db import models

from multi_email_field.fields import MultiEmailField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class EmailPartial(models.Model):
    subject = models.CharField(
        max_length=255
    )
    from_address = models.EmailField()
    to_addresses = MultiEmailField()
    message = models.TextField()
    fail_silently = models.BooleanField(
        default=True
    )

    panels = [
        FieldPanel('subject', classname="full"),
        FieldPanel('from_address', classname="full"),
        FieldPanel('to_addresses', classname="full"),
        FieldPanel('message', classname="full"),
        FieldPanel('fail_silently'),
    ]

    class Meta:
        abstract = True

    def send_form_mail(self, form):
        content = [self.message, '', ]

        for name, field in form.fields.items():
            data = form.cleaned_data.get(name)
            if name == 'recaptcha' or not data:
                continue
            content.append(field.label + ': ' + six.text_type(data))

        send_mail(
            self.subject,
            '\n'.join(content),
            self.from_address,
            self.to_addresses,
            self.fail_silently
        )
