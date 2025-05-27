from wagtailstreamforms.blocks import InfoBlock

from ..test_case import AppTestCase


class TestInfoBlockTestCase(AppTestCase):
    def test_form_render_with_value(self):
        block = InfoBlock()

        test_form_html = block.render_form("foo")
        expected_html = "\n".join(
            ['<div style="margin-top:5px;padding:0.9em 1.2em;">foo</div>']
        )
        self.assertInHTML(expected_html, test_form_html)

    def test_form_render_no_value_with_help_text(self):
        block = InfoBlock(help_text="some help")

        test_form_html = block.render_form("")
        expected_html = "\n".join(
            ['<div style="margin-top:5px;padding:0.9em 1.2em;">some help</div>']
        )
        self.assertInHTML(expected_html, test_form_html)

    def test_form_render_value_and_help_text(self):
        block = InfoBlock(help_text="some help")

        test_form_html = block.render_form("foo")
        expected_html = "\n".join(
            ['<div style="margin-top:5px;padding:0.9em 1.2em;">foo</div>']
        )
        self.assertInHTML(expected_html, test_form_html)
