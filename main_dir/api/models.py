from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(BaseModel):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField(unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def clean_latitude(self):
        if self.latitude < -90.0 or self.latitude > 90.0:
            raise ValidationError(
                'Неверная широта. Допустимое значение от -90.0 до 90.0.'
            )

    def clean_longitude(self):
        if self.longitude < -180.0 or self.longitude > 180.0:
            raise ValidationError(
                'Неверная долгота. Допустимое значение от -180.0 до 180.0.'
            )

    def clean(self):
        self.clean_latitude()
        self.clean_longitude()
