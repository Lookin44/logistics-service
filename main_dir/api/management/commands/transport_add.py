import logging
import random
import string

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from api.models import Transport


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Создание транспорта'

    def handle(self, *args, **options):
        transport_count = Transport.objects.count()
        target_count = 20

        if transport_count >= target_count:
            logger.info(f'В базе данных {transport_count} единиц транспорта.')
            return None

        diff_count = target_count - transport_count

        while diff_count > 0:
            first_symbol = str(random.randint(1, 9))
            second_symbol = str(random.randint(0, 9))
            third_symbol = str(random.randint(0, 9))
            forth_symbol = str(random.randint(0, 9))
            fifth_symbol = random.choice(string.ascii_uppercase)
            symbol_arr = [
                first_symbol,
                second_symbol,
                third_symbol,
                forth_symbol,
                fifth_symbol,
            ]
            uniq_number = ''.join(symbol_arr)
            tonnage = random.randint(1, 1000)
            try:
                Transport.objects.create(number=uniq_number, tonnage=tonnage)
                diff_count -= 1
            except IntegrityError:
                logger.error(
                    f'Транспорт с номером {uniq_number} уже существует'
                )
        logger.info(
            f'Было добавлено {target_count - transport_count} единиц '
            f'транспорта'
        )
