import urllib.parse as urlparse

from ..test_case import AppTestCase


class TemplateTagTests(AppTestCase):
    def test_kwarg_added(self):
        fake_request = self.rf.get("/")
        rendered = self.render_template(
            "{% load streamforms_tags %}?{% url_replace page=1 %}",
            {"request": fake_request},
        )
        # parse the url as they can be reordered unpredictably
        parsed = urlparse.parse_qs(urlparse.urlparse(rendered).query)
        self.assertDictEqual(parsed, {"page": ["1"]})

    def test_kwarg_appended(self):
        fake_request = self.rf.get("/?foo=bar")
        rendered = self.render_template(
            "{% load streamforms_tags %}?{% url_replace page=1 %}",
            {"request": fake_request},
        )
        # parse the url as they can be reordered unpredictably
        parsed = urlparse.parse_qs(urlparse.urlparse(rendered).query)
        self.assertDictEqual(parsed, {"foo": ["bar"], "page": ["1"]})

    def test_kwarg_replaced(self):
        fake_request = self.rf.get("/?foo=bar&page=1")
        rendered = self.render_template(
            "{% load streamforms_tags %}?{% url_replace page=5 %}",
            {"request": fake_request},
        )
        # parse the url as they can be reordered unpredictably
        parsed = urlparse.parse_qs(urlparse.urlparse(rendered).query)
        self.assertDictEqual(parsed, {"foo": ["bar"], "page": ["5"]})
