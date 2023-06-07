import random
import logging

from celery import shared_task

from .models import Transport, Location


logger = logging.getLogger(__name__)


@shared_task
def change_transport_location():
    transport = Transport.objects.all()
    locations = Location.objects.all()
    if not transport:
        logger.error('В базе данных отсутствует транспорт')

    for unit in transport:
        new_location = random.choice(locations)
        unit.current_location = new_location
        unit.save()
        logger.info(f'У транспорта {unit} изменена локация')
