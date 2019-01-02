from wagtail.core import blocks


class CollapsibleStructBlock(blocks.StructBlock):
    COLLAPSIBLE = 'COLLAPSIBLE'

    def get_layout(self):
        return self.COLLAPSIBLE
