from geopy.distance import geodesic
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Cargo, Location, Transport


class CargoSerializer(serializers.ModelSerializer):

    location_up = serializers.SlugRelatedField(
        slug_field='zip_code',
        queryset=Location.objects.all()
    )
    location_delivery = serializers.SlugRelatedField(
        slug_field='zip_code',
        queryset=Location.objects.all()
    )
    number_of_nearest_transport = SerializerMethodField(
        method_name='filter_transport'
    )

    class Meta:
        model = Cargo
        fields = [
            'description',
            'location_up',
            'location_delivery',
            'number_of_nearest_transport',
        ]


    def filter_transport(self, obj: Cargo) -> int:
        """
        Метод подсчитывающий количество близлежащего транспорта
        """
        count = 0
        transports = Transport.objects.select_related('current_location')
        location_up = (
            obj.location_up.latitude,
            obj.location_up.longitude
        )
        for unit in transports:
            lat = unit.current_location.latitude
            long = unit.current_location.longitude
            unit_location = (lat, long)
            if geodesic(location_up, unit_location).mi <= 450:
                count += 1

            return count


class CargoDetailSerializer(serializers.ModelSerializer):
    location_up = serializers.SlugRelatedField(
        slug_field='zip_code',
        queryset=Location.objects.all()
    )
    location_delivery = serializers.SlugRelatedField(
        slug_field='zip_code',
        queryset=Location.objects.all()
    )
    transport = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = [
            'pk',
            'location_up',
            'location_delivery',
            'description',
            'weight',
            'transport'
        ]
        read_only_fields = ['pk', 'transport']

    def get_transport(self, obj):
        """
        Метод собирающий список транспорта с дистанцией до груза
        """
        transport_list = []
        location_up = (
            obj.location_up.latitude,
            obj.location_up.longitude
        )
        transports = Transport.objects.select_related('current_location')

        for unit in transports:
            lat = unit.current_location.latitude
            long = unit.current_location.longitude
            unit_location = (lat, long)
            distance = geodesic(location_up, unit_location).mi
            unit_detail = {
                'number': unit.number,
                'distance': round(distance, 3)
            }
            transport_list.append(unit_detail)
        return sorted(transport_list, key=lambda x: x['distance'])

    def update(self, instance, validated_data):

        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.save()
        return instance


class TransportSerializer(serializers.ModelSerializer):
    current_location = serializers.SlugRelatedField(
        slug_field='zip_code',
        queryset=Location.objects.all()
    )

    class Meta:
        model = Transport
        fields = ['pk', 'current_location', 'number', 'tonnage']
        read_only_fields = ['pk', 'number', 'tonnage']

    def update(self, instance, validated_data):
        instance.current_location = validated_data.get(
            'current_location',
            instance.current_location
        )
        instance.save()
        return instance
