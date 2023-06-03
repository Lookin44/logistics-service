import random
import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(BaseModel):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField(unique=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(
                -90.0,
                'Широта не может быть ниже -90 градусов.'
            ),
            MaxValueValidator(
                90.0,
                'Широта не может быть выше 90 градусов.'
            )
        ]
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(
                -180.0,
                'Долгота не может быть ниже -180 градусов.'
            ),
            MaxValueValidator(
                180.0,
                'Долгота не может быть выше 180 градусов.'
            )
        ]
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        ordering = ['pk']

    def __str__(self):
        return f'{self.city} - {self.state}'


class Transport(BaseModel):
    number = models.CharField(max_length=5, unique=True)
    current_location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
    )
    tonnage = models.IntegerField(
        validators=[
            MinValueValidator(1, 'Вес не может быть ниже 1.'),
            MaxValueValidator(1000, 'Вес не может превышать 1000.')
        ]
    )

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорты'
        ordering = ['pk']

    @staticmethod
    def random_location():
        random_location = random.choice(Location.objects.all())
        return random_location

    def clean_transport_number(self):
        pattern = r'^(?:[1-9][0-9]{2}[1-9]|[1-9][0-9]{3}[A-Z])$'
        if not re.match(pattern, self.number):
            raise ValidationError(
                'Неверный формат номера. Формат номера выглядит следующим '
                'образом: первые четыре цифры в диапазоне от 1000 до 9999, '
                'затем одна заглавная буква английского алфавита. Пример: '
                '1234A, 2534B, 9999Z'
            )

        number_value = int(self.number[:-1])
        if not (1000 <= number_value <= 9999):
            raise ValidationError(
                'Числовая часть номера должна быть в диапазоне от 1000 до 9999'
            )

    def clean(self):
        self.clean_transport_number()

    def save(self, *args, **kwargs):
        if not self.current_location:
            self.current_location = self.random_location()
            super().save(*args, **kwargs)
