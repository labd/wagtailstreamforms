from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from wagtailstreamforms.models import FormSubmission


class Command(BaseCommand):
    help = "Deletes form submissions older than the provided number of days"

    def add_arguments(self, parser):
        parser.add_argument("days_to_keep", type=int)

    def get_queryset(self, date):
        return FormSubmission.objects.filter(submit_time__lt=date)

    def handle(self, *args, **options):
        keep_from_date = datetime.today().date() - timedelta(days=options["days_to_keep"])

        queryset = self.get_queryset(keep_from_date)

        count = queryset.count()
        queryset.delete()

        msg = "Successfully deleted %s form submissions prior to %s" % (
            count,
            keep_from_date,
        )
        self.stdout.write(self.style.SUCCESS(msg))
