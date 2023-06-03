import random
import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        db_index=True,
        default=timezone.now,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class Location(BaseModel):
    city = models.CharField(
        max_length=100,
        verbose_name='Город / Населенный пункт',
    )
    state = models.CharField(
        max_length=100,
        verbose_name='Штат / Область',
    )
    postcode = models.IntegerField(
        unique=True,
        verbose_name='Почтовый индекс',
    )
    latitude = models.DecimalField(
        verbose_name='Широта',
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(
                -90.0,
                'Широта не может быть ниже -90 градусов.',
            ),
            MaxValueValidator(
                90.0,
                'Широта не может быть выше 90 градусов.',
            ),
        ],
    )
    longitude = models.DecimalField(
        verbose_name='Долгота',
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(
                -180.0,
                'Долгота не может быть ниже -180 градусов.',
            ),
            MaxValueValidator(
                180.0,
                'Долгота не может быть выше 180 градусов.',
            ),
        ],
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        ordering = ['pk']

    def __str__(self):
        return f'{self.city} - {self.state}'


class Transport(BaseModel):
    number = models.CharField(
        verbose_name='Гос. номер транспорта',
        max_length=5,
        validators=[
            RegexValidator(
                r'^(?:[1-9][0-9]{2}[1-9]|[1-9][0-9]{3}[A-Z])$',
                'Неверный формат номера.',
            ),
        ],
        unique=True,
        help_text='Первые четыре цифры в диапазоне от 1000 до 9999, затем '
                  'одна заглавная буква английского алфавита. Пример: 1234A, '
                  '2534B, 9999Z'
    )
    current_location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Локация',
        related_name='locations',
    )
    tonnage = models.PositiveIntegerField(
        verbose_name='Доступный вес',
        help_text='Допустимое значение от 1 до 1000',
        validators=[
            MinValueValidator(1, 'Вес не может быть ниже 1.'),
            MaxValueValidator(1000, 'Вес не может превышать 1000.'),
        ],
    )

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорты'
        ordering = ['pk']

    @staticmethod
    def random_location():
        random_location = random.choice(Location.objects.all())
        return random_location

    def save(self, *args, **kwargs):
        if not self.current_location:
            self.current_location = self.random_location()
            super().save(*args, **kwargs)


class Cargo(BaseModel):
    location_up = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
        related_name='up_locations',
        verbose_name='Локация загрузки',
        help_text='Выберите место загрузки.',
    )
    location_delivery = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
        related_name='down_locations',
        verbose_name='Локация разгрузки',
        help_text='Выберите место разгрузки.',
    )
    weight = models.PositiveIntegerField(
        verbose_name='Вес',
        help_text='Допустимое значение от 1 до 1000',
        validators=[
            MinValueValidator(1, 'Вес не может быть ниже 1.'),
            MaxValueValidator(1000, 'Вес не может превышать 1000.'),
        ],
    )
    description = models.CharField(
        verbose_name='Описание товара',
        help_text='Введите небольшое описание товара, для курьера.',
    )

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'
        ordering = ['pk']
