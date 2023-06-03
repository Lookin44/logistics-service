from django.contrib import admin
from .models import Location, Transport


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'city',
        'state',
        'postcode',
        'latitude',
        'longitude',
    )


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'number',
        'current_location',
        'tonnage',
    )
    exclude = ('current_location', )

