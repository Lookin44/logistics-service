from django.contrib import admin
from .models import Location, Transport, Cargo


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


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'location_up',
        'location_delivery',
        'weight',
        'description',
    )
