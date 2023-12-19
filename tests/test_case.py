import sys
from contextlib import contextmanager
from importlib import import_module, reload

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection, models
from django.template import Context, Template
from django.test import TestCase
from django.test.client import RequestFactory


class AppTestCase(TestCase):
    @property
    def rf(self):
        return RequestFactory()

    @staticmethod
    def setupModels(*models):
        """Create test models"""
        with connection.schema_editor(atomic=True) as schema_editor:
            for model in models:
                schema_editor.create_model(model)

    def get_field(self, modelClass, name):
        return modelClass._meta.get_field(name)

    def get_file(self):
        return SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")

    @contextmanager
    def register_field(self, field_type, cls):
        from wagtailstreamforms import fields

        fields.register(field_type, cls)
        try:
            yield
        finally:
            fields._fields[field_type].remove(cls)

    @contextmanager
    def register_hook(self, hook_name, fn, order=0):
        from wagtailstreamforms import hooks

        hooks.register(hook_name, fn, order)
        try:
            yield
        finally:
            hooks._hooks[hook_name].remove((fn, order))

    def reload_module(self, path):
        if path in sys.modules:
            reload(sys.modules[path])
        return import_module(path)

    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    _non_blankable_fields = [models.BooleanField]

    def assertModelField(self, field, expected_class, null=False, blank=False, default=None):
        self.assertEqual(field.__class__, expected_class)
        self.assertEqual(field.null, null)
        if expected_class not in self._non_blankable_fields:
            self.assertEqual(field.blank, blank)

        if default:
            self.assertEqual(field.default, default)

    def assertModelDecimalField(self, field, max_digits, decimal_places, null=False, blank=False):
        self.assertEqual(field.__class__, models.DecimalField)
        self.assertEqual(field.max_digits, max_digits)
        self.assertEqual(field.decimal_places, decimal_places)
        self.assertEqual(field.null, null)
        self.assertEqual(field.blank, blank)

    def assertModelPKField(
        self, field, rel_to, on_delete, null=False, blank=False, related_name=None
    ):
        self.assertEqual(field.__class__, models.ForeignKey)
        self.assertEqual(field.remote_field.model, rel_to)
        self.assertEqual(field.remote_field.on_delete, on_delete)
        self.assertEqual(field.null, null)
        self.assertEqual(field.blank, blank)

        if related_name:
            self.assertEqual(field.remote_field.related_name, related_name)
