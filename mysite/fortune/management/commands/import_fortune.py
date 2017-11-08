"""Command for importing the "fortunes"."""
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from fortune.models import Category, Fortune

from os import path


class Command(BaseCommand):
    """The fortune importer class."""
    help = 'Import fortunes from a file.'

    def add_arguments(self, parser):
        """Add the arguments "file" and "category" to the parser."""
        parser.add_argument('file', type=str)
        parser.add_argument('-c', '--category', type=str,
                            dest='category', default='',
                            help='Specify a category name for the fortunes.' + \
                                 ' (Default: file name)')

    def handle(self, *args, **options):
        """Import the fortunes to the database."""
        self.stdout.write('Start importing the file.')

        # Set category
        category = options['category']
        if not category:
            category = path.basename(options['file'])
            category = path.splitext(category)[0]
            self.stdout.write(self.style.WARNING(
                'Using the name: ' + category +' as name.'))

        category = Category.objects.get_or_create(category=category)[0]

        with open(options['file'], 'r') as file:
            fortunes = file.read()
            for fortune in fortunes.split('\n%\n'):
                if fortune:
                    try:
                        Fortune.objects.create(text=fortune,
                                               category=category)
                    except IntegrityError:
                        self.stdout.write(self.style.ERROR(
                            'Fortune already exists!'))
        self.stdout.write(self.style.SUCCESS(
            'Fortunes has been imported!'))
