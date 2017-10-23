from wagtailstreamforms.models import BaseForm, BasicForm

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(BasicForm, BaseForm))


class ModelPropertyTests(AppTestCase):

    def test_form(self, store_submission=False):
        return BasicForm.objects.create(
            name='Form',
            template_name='streamforms/form_block.html',
            store_submission=store_submission
        )

    def test_specific(self):
        form = self.test_form()
        self.assertEquals(form.specific, form)
        self.assertEquals(BaseForm.objects.get(pk=form.pk).specific, form)

    def test_specific_class(self):
        form = self.test_form()
        self.assertEquals(form.specific_class, form.__class__)
        self.assertEquals(BaseForm.objects.get(pk=form.pk).specific_class, form.__class__)