from django.test import override_settings

from wagtailstreamforms import hooks
from wagtailstreamforms.wagtailstreamforms_hooks import save_form_submission_data

from ..test_case import AppTestCase


def test_hook():
    pass


class TestHookRegistering(AppTestCase):

    @classmethod
    def setUpClass(cls):
        hooks.register('test_hook_name', test_hook)

    @classmethod
    def tearDownClass(cls):
        del hooks._hooks['test_hook_name']

    def test_before_hook(self):
        def before_hook():
            pass

        with self.register_hook('test_hook_name', before_hook, order=-1):
            hook_fns = hooks.get_hooks('test_hook_name')
            self.assertEqual(hook_fns, [before_hook, test_hook])

    def test_after_hook(self):
        def after_hook():
            pass

        with self.register_hook('test_hook_name', after_hook, order=1):
            hook_fns = hooks.get_hooks('test_hook_name')
            self.assertEqual(hook_fns, [test_hook, after_hook])


class TestHookDefaults(AppTestCase):

    def test_default_hooks(self):
        hook_fns = hooks.get_hooks('process_form_submission')
        self.assertEqual(hook_fns, [save_form_submission_data])

    @override_settings(WAGTAILSTREAMFORMS_ENABLE_BUILTIN_HOOKS=False)
    def test_builtins_can_be_disabled(self):
        hook_fns = hooks.get_hooks('process_form_submission')
        self.assertEqual(hook_fns, [])

    @override_settings(WAGTAILSTREAMFORMS_ENABLE_BUILTIN_HOOKS=False)
    def test_setting_only_removes_builtins(self):
        def custom_hook():
            pass

        with self.register_hook('process_form_submission', custom_hook, order=1):
            hook_fns = hooks.get_hooks('process_form_submission')
            self.assertEqual(hook_fns, [custom_hook])
