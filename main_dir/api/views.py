from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .filters import CargoFilter
from .models import Cargo, Transport
from .serializers import (
    CargoSerializer,
    CargoDetailSerializer,
    TransportSerializer
)


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.select_related(
            'location_up',
            'location_delivery'
    )
    serializer_class = CargoDetailSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_class = CargoFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return CargoSerializer
        elif self.action == 'retrieve':
            return CargoDetailSerializer
        return super().get_serializer_class()


class TransportViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.select_related(
        'current_location',
    )
    serializer_class = TransportSerializer
    http_method_names = ['get', 'patch']
