import random
import logging

from celery import shared_task

from .models import Transport, Location


logger = logging.getLogger(__name__)


@shared_task
def change_transport_location():
    query = Transport.objects.all()
    locations = Location.objects.all()
    if not query:
        logger.error('В базе данных отсутствует транспорт')

    for unit in query:
        unit.current_location = random.choice(locations)
        unit.save()
        logger.info(f'У транспорта {unit} изменена локация')
