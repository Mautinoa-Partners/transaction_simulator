from django.core.management.base import NoneCommand


class Command(NoneCommand):
    help = "Presumes downloaded geodatabase for GADM."

    def add_arguments(self, parser):
        parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        raise NotImplementedError()
