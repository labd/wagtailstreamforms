from django.core import serializers
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import CheckboxSelectMultiple
from wagtailstreamforms.fields import HookMultiSelectFormField, HookSelectField

from ..models import HookSelectModel
from ..test_case import AppTestCase


class HookSelectFieldTests(AppTestCase):
    def test_default_choices_has_in_app_hooks(self):
        field = self.get_field(HookSelectModel, "hooks")
        self.assertEqual(
            field.get_choices_default(),
            [("save_form_submission_data", "Save form submission data")],
        )

    def test_registering_hook_adds_that_as_a_choice(self):
        def before_hook():
            pass

        with self.register_hook("process_form_submission", before_hook, order=-1):
            field = self.get_field(HookSelectModel, "hooks")
            self.assertEqual(
                field.get_choices_default(),
                [
                    ("before_hook", "Before hook"),
                    ("save_form_submission_data", "Save form submission data"),
                ],
            )

    def test_db_prep_save(self):
        field = HookSelectField("test")
        field.set_attributes_from_name("hooks")
        self.assertEqual(None, field.get_db_prep_save(None, connection=None))
        self.assertEqual(
            "do_foo,do_bar",
            field.get_db_prep_save(["do_foo", "do_bar"], connection=None),
        )

    def test_to_python(self):
        field = HookSelectField()
        self.assertEqual(field.to_python(None), [])
        self.assertEqual(field.to_python(""), [])
        self.assertEqual(field.to_python(["do_foo", "do_bar"]), ["do_foo", "do_bar"])
        self.assertEqual(field.to_python("do_foo,do_bar"), ["do_foo", "do_bar"])

    def test_formfield(self):
        field = self.get_field(HookSelectModel, "hooks")
        formfield = field.formfield()
        self.assertTrue(isinstance(formfield, HookMultiSelectFormField))
        self.assertTrue(isinstance(formfield.widget, CheckboxSelectMultiple))
        self.assertEqual(
            formfield.choices,
            [("save_form_submission_data", "Save form submission data")],
        )

    def test_serialisation(self):
        hooks = ["do_foo", "do_bar"]
        obj = next(
            serializers.deserialize(
                "json", serializers.serialize("json", [HookSelectModel(hooks=hooks)])
            )
        ).object
        self.assertEqual(obj.hooks, hooks)

    def test_value(self):
        obj = HookSelectModel(hooks=["save_form_submission_data"])
        self.assertEqual(obj.hooks, ["save_form_submission_data"])

    def test_empty(self):
        obj = HookSelectModel(hooks="")
        self.assertEqual(obj.hooks, "")

    def test_empty_list(self):
        obj = HookSelectModel(hooks=[])
        self.assertEqual(obj.hooks, [])

    def test_null(self):
        obj = HookSelectModel(hooks=None)
        self.assertEqual(obj.hooks, None)

    def test_validate(self):
        # invalid choice
        obj = HookSelectModel(hooks=["do_woop"])
        self.assertRaises(ValidationError, obj.full_clean)

        # valid
        obj = HookSelectModel(hooks=["save_form_submission_data"])
        obj.full_clean()

    def test_save(self):
        HookSelectModel.objects.create(id=10, hooks=["save_form_submission_data"])
        obj = HookSelectModel.objects.get(id=10)
        self.assertEqual(obj.hooks, ["save_form_submission_data"])

    def test_save_empty(self):
        HookSelectModel.objects.create(id=10, hooks="")
        obj = HookSelectModel.objects.get(id=10)
        self.assertEqual(obj.hooks, [])

    def test_save_empty_list(self):
        HookSelectModel.objects.create(id=10, hooks=[])
        obj = HookSelectModel.objects.get(id=10)
        self.assertEqual(obj.hooks, [])

    def test_save_null(self):
        HookSelectModel.objects.create(id=10, hooks=None)
        obj = HookSelectModel.objects.get(id=10)
        self.assertEqual(obj.hooks, [])
