from wagtail.core.fields import StreamField

from wagtailstreamforms.fields import get_fields


class FormFieldsStreamField(StreamField):

    def __init__(self, block_types, **kwargs):
        block_types = [(key, item().get_form_block()) for key, item in get_fields().items()]
        super().__init__(block_types, **kwargs)
