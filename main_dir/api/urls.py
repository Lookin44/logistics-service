from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import CargoViewSet, TransportViewSet


router = SimpleRouter()
router.register('cargos', CargoViewSet, basename='cargos')
router.register('transport', TransportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
