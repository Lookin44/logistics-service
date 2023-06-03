import csv
import os
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from api.models import Location


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Заполнение таблицы стандартными локациями'

    def handle(self, *args, **options):
        locations_list = []
        try:
            file_path = os.path.join(settings.BASE_DIR, 'uszips.csv')
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    postcode = int(row['zip'])
                    latitude = float(row['lat'])
                    longitude = float(row['lng'])
                    city = row['city']
                    state = row['state_name']
                    locations_list.append(Location(
                        city=city,
                        state=state,
                        postcode=postcode,
                        latitude=latitude,
                        longitude=longitude,
                    ))
            Location.objects.bulk_create(locations_list)
            logger.info('Добавлены базовые локации.')
        except FileNotFoundError:
            logger.error(
                'Отсутствует файл со стандартными локациями. '
                'Проверьте что файл uszips.csv находиться в директории '
                'main_dir.'
            )
        except IntegrityError:
            logger.error(
                'Встретились дубликаты записей. Вероятно локации уже '
                'загружены в базу данных.'
            )
