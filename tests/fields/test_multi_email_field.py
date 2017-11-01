from django.core.exceptions import ValidationError
from django.db import models

from wagtailstreamforms.fields import MultiEmailField
from wagtailstreamforms.forms import MultiEmailField as MultiEmailFormField
from wagtailstreamforms.widgets import MultiEmailWidget

from ..test_case import AppTestCase


class MultiEmailModel(models.Model):
    emails = MultiEmailField(null=True)

    class Meta:
        app_label = 'tests'


class MultiEmailModelFieldTests(AppTestCase):

    def test_email_field(self):
        obj = MultiEmailModel(emails=['foo@foo.com', 'bar@bar.com'])
        self.assertEqual(obj.emails, ['foo@foo.com', 'bar@bar.com'])

    def test_email_field_empty(self):
        obj = MultiEmailModel(emails='')
        self.assertEqual(obj.emails, '')

    def test_email_field_empty_list(self):
        obj = MultiEmailModel(emails=[])
        self.assertEqual(obj.emails, [])

    def test_email_field_null(self):
        obj = MultiEmailModel(emails=None)
        self.assertEqual(obj.emails, None)

    def test_email_field_save(self):
        MultiEmailModel.objects.create(
            id=10,
            emails=['foo@foo.com', 'bar@bar.com'],
        )
        obj2 = MultiEmailModel.objects.get(id=10)
        self.assertEqual(obj2.emails, ['foo@foo.com', 'bar@bar.com'])

    def test_email_field_save_empty(self):
        MultiEmailModel.objects.create(id=10, emails='')
        obj2 = MultiEmailModel.objects.get(id=10)
        self.assertEqual(obj2.emails, [])

    def test_email_field_save_empty_list(self):
        MultiEmailModel.objects.create(id=10, emails=[])
        obj2 = MultiEmailModel.objects.get(id=10)
        self.assertEqual(obj2.emails, [])

    def test_email_field_save_null(self):
        MultiEmailModel.objects.create(id=10, emails=None)
        obj2 = MultiEmailModel.objects.get(id=10)
        self.assertEqual(obj2.emails, [])

    def test_db_prep_save(self):
        field = MultiEmailField("test")
        field.set_attributes_from_name("emails")
        self.assertEqual(None, field.get_db_prep_save(None, connection=None))
        self.assertEqual(
            'foo@foo.com\nbar@bar.com',
            field.get_db_prep_save(['foo@foo.com', 'bar@bar.com'], connection=None)
        )

    def test_formfield(self):
        field = MultiEmailField("test")
        field.set_attributes_from_name("emails")
        formfield = field.formfield()
        self.assertEqual(type(formfield), MultiEmailFormField)
        self.assertEqual(type(formfield.widget), MultiEmailWidget)

    def test_to_python(self):
        field = MultiEmailField()
        self.assertEqual(field.to_python(None), [])
        self.assertEqual(field.to_python(''), [])
        self.assertEqual(field.to_python(['foo@foo.com', 'bar@bar.com']), ['foo@foo.com', 'bar@bar.com'])
        self.assertEqual(field.to_python('foo@foo.com\nbar@bar.com'), ['foo@foo.com', 'bar@bar.com'])


class MultiEmailFormFieldTest(AppTestCase):

    def test__widget(self):
        f = MultiEmailFormField()
        self.assertIsInstance(f.widget, MultiEmailWidget)

    def test__to_python(self):
        f = MultiEmailFormField()

        # Empty values
        for val in ['', None]:
            self.assertEqual([], f.to_python(val))

        # One line correct value
        val = '  foo@bar.com    '
        self.assertEqual(['foo@bar.com'], f.to_python(val))

        # Multi lines correct values (test of #0010614)
        val = 'foo@bar.com\nfoo2@bar2.com\r\nfoo3@bar3.com'
        self.assertEqual(['foo@bar.com', 'foo2@bar2.com', 'foo3@bar3.com'], f.to_python(val))

    def test__validate(self):
        f = MultiEmailFormField(required=True)

        # Empty value
        val = []
        self.assertRaises(ValidationError, f.validate, val)

        # Incorrect value
        val = ['not-an-email.com']
        self.assertRaises(ValidationError, f.validate, val)

        # An incorrect value with correct values
        val = ['foo@bar.com', 'not-an-email.com', 'foo3@bar3.com']
        self.assertRaises(ValidationError, f.validate, val)

        # Should not happen (to_python do the strip)
        val = ['  foo@bar.com    ']
        self.assertRaises(ValidationError, f.validate, val)

        # Correct value
        val = ['foo@bar.com']
        f.validate(val)


class MultiEmailWidgetTest(AppTestCase):

    def test__prep_value__empty(self):
        w = MultiEmailWidget()
        value = w.prep_value('')
        self.assertEqual(value, '')

    def test__prep_value__string(self):
        w = MultiEmailWidget()
        value = w.prep_value('foo@foo.fr\nbar@bar.fr')
        self.assertEqual(value, 'foo@foo.fr\nbar@bar.fr')

    def test__prep_value__list(self):
        w = MultiEmailWidget()
        value = w.prep_value(['foo@foo.fr', 'bar@bar.fr'])
        self.assertEqual(value, 'foo@foo.fr\nbar@bar.fr')

    def test__prep_value__raise(self):
        w = MultiEmailWidget()
        self.assertRaises(ValidationError, w.prep_value, 42)

    def test__render(self):
        w = MultiEmailWidget()
        output = w.render('test', ['foo@foo.fr', 'bar@bar.fr'])
        expected_html = '<textarea name="test" cols="40" rows="10">\nfoo@foo.fr\nbar@bar.fr</textarea>'
        self.assertHTMLEqual(output, expected_html)
