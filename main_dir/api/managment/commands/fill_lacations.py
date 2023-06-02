import csv

from django.core.management.base import BaseCommand

from api.models import Location


class Command(BaseCommand):

    help = 'Заполнение таблицы стандартными локациями'

    def handle(self, *args, **options):
        with open('main_dir/uszips.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                zip_code = row['zip']
                latitude = float(row['lat'])
                longitude = float(row['lng'])
                city = row['city']
                state = row['state_name']
                location = Location(zip_code=zip_code, latitude=latitude,
                                    longitude=longitude, city=city,
                                    state=state)
                location.save()
