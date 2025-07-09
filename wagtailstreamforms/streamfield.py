from django.core.exceptions import ImproperlyConfigured
from wagtail import blocks
from wagtail.fields import StreamField

from wagtailstreamforms.fields import BaseField, get_fields


class FormFieldStreamBlock(blocks.StreamBlock):
    """Add all registered instances of BaseField's get_form_block method to the streamfield."""

    def __init__(self, local_blocks=None, **kwargs) -> None:
        self._constructor_kwargs = kwargs

        # Note, this is calling BaseStreamBlock's super __init__, not FormFieldStreamBlock's.
        # We don't want BaseStreamBlock.__init__() to run, because it tries to assign to
        # self.child_blocks, which we've overridden with a @property. But we DO want
        # Block.__init__() to run.
        super(blocks.BaseStreamBlock, self).__init__()

        self._child_blocks = self.base_blocks.copy()

        for name, field_class in get_fields().items():
            # ensure the field is a subclass of BaseField.
            if not issubclass(field_class, BaseField):
                raise ImproperlyConfigured(
                    "'%s' must be a subclass of '%s'" % (field_class, BaseField)
                )

            # assign the block
            block = field_class().get_form_block()
            block.set_name(name)
            self._child_blocks[name] = block

        self._dependencies = self._child_blocks.values()

    @property
    def child_blocks(self):
        return self._child_blocks

    @property
    def dependencies(self):
        return self._dependencies


class FormFieldsStreamField(StreamField):
    def __init__(self, block_types, **kwargs) -> None:
        super().__init__(block_types, **kwargs)
        self.stream_block = FormFieldStreamBlock(block_types, required=not self.blank)
