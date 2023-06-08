from django_filters import rest_framework

from .models import Cargo


class CargoFilter(rest_framework.FilterSet):

    class Meta:
        model = Cargo
        fields = {
            'weight': ['lte'],
        }


class CargoDistanceFilter(rest_framework.FilterSet):

    distance = rest_framework.NumberFilter(
        field_name='distance',
        method='transport_distance'
    )

    class Meta:
        model = Cargo
        fields = ('distance', )

        def transport_distance(self, queryset, name, value):
            print(self.__dict__)
            return queryset
