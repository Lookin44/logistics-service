from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .filters import CargoFilter, CargoDistanceFilter
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
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_class = CargoFilter
    serializer_class = CargoSerializer

    def get_serializer_class(self):

        if self.action == 'list':
            return CargoSerializer
        elif self.action == 'retrieve':
            return CargoDetailSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        distance = self.request.query_params.get('distance')
        context.update({'distance': distance})
        return context


class TransportViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.select_related(
        'current_location',
    )
    serializer_class = TransportSerializer
    http_method_names = ['get', 'patch']
