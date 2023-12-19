from django.core.management import call_command

from tests.test_case import AppTestCase


class Tests(AppTestCase):
    fixtures = ["test"]

    def test_migrations(self):
        call_command("makemigrations", dry_run=True, check=True)
