from django_filters import rest_framework

from .models import Cargo


class CargoFilter(rest_framework.FilterSet):

    weight = rest_framework.NumberFilter(
        field_name='weight',
        lookup_expr='lte'
    )

    class Meta:
        model = Cargo
        fields = ('weight', )
