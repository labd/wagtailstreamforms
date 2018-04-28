import json

from django.core.serializers.json import DjangoJSONEncoder

from wagtailstreamforms.hooks import register


@register('process_form_submission')
def save_form_submission_data(instance, form):
    """ saves the form submission data """

    instance.get_submission_class().objects.create(
        form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
        form=instance
    )
