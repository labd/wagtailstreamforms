from wagtailstreamforms.models import BaseForm, BasicForm, FormField

from ..test_case import AppTestCase


class ModelGenericTests(AppTestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(BasicForm, BaseForm))


class ModelPropertyTests(AppTestCase):

    def test_form(self, store_submission=False):
        form = BasicForm.objects.create(
            name='Form',
            slug='form',
            template_name='streamforms/form_block.html',
            store_submission=store_submission
        )
        FormField.objects.create(
            form=form,
            label='name',
            field_type='singleline'
        )
        return form

    def test_copy_is_right_class(self):
        form = self.test_form()

        copied = BaseForm.objects.get(pk=form.pk).copy()

        self.assertNotEquals(copied.pk, form.pk)
        self.assertEquals(copied.specific_class, form.specific_class)

    def test_specific(self):
        form = self.test_form()
        self.assertEquals(form.specific, form)
        self.assertEquals(BaseForm.objects.get(pk=form.pk).specific, form)

    def test_specific_class(self):
        form = self.test_form()
        self.assertEquals(form.specific_class, form.__class__)
        self.assertEquals(BaseForm.objects.get(pk=form.pk).specific_class, form.__class__)