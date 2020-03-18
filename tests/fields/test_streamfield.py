from django import forms
from django.core.exceptions import ImproperlyConfigured
from wagtailstreamforms import fields
from wagtailstreamforms.streamfield import FormFieldsStreamField

from ..test_case import AppTestCase


class GoodField(fields.BaseField):
    field_class = forms.CharField


class TestCorrectTypeRegistering(AppTestCase):
    @classmethod
    def setUpClass(cls):
        fields.register("good", GoodField)

    @classmethod
    def tearDownClass(cls):
        del fields._fields["good"]

    def test_child_blocks(self):
        field = FormFieldsStreamField([])
        self.assertIn("good", field.stream_block.child_blocks)

    def test_dependencies(self):
        field = FormFieldsStreamField([])
        self.assertListEqual(
            [b.__class__ for b in field.stream_block.dependencies],
            [b.__class__ for b in field.stream_block.child_blocks.values()],
        )


class BadField:
    field_class = forms.CharField


class TestIncorrectTypeRegistering(AppTestCase):
    @classmethod
    def setUpClass(cls):
        fields.register("bad", BadField)

    @classmethod
    def tearDownClass(cls):
        del fields._fields["bad"]

    def test_is_invalid_class(self):
        expected_error = "'%s' must be a subclass of '%s'" % (
            BadField,
            fields.BaseField,
        )

        with self.assertRaises(ImproperlyConfigured) as e:
            FormFieldsStreamField([])

        self.assertEqual(e.exception.args[0], expected_error)
