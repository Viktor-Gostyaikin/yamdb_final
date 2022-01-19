import csv

from django.core.management.base import BaseCommand

import requests
from reviews.models import Genre


class Command(BaseCommand):
    help = 'Loading data from csv via url'

    def add_arguments(self, parser):
        parser.add_argument('link', type=str)

    def handle(self, link: str, *args, **options):
        response = requests.get(link)
        reader = csv.DictReader(response.text.splitlines())

        Genre.objects.bulk_create(
            [Genre(
                **{k.lower(): v for k, v in data.items()}
            ) for data in reader])

        self.stdout.write(self.style.SUCCESS('Successfully loaded'))
