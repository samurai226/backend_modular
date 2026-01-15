"""
URLs Transport
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompagnieViewSet, BusViewSet, TrajetViewSet,
    PlaceViewSet, ReservationViewSet
)

router = DefaultRouter()
router.register(r'compagnies', CompagnieViewSet, basename='compagnie')
router.register(r'bus', BusViewSet, basename='bus')
router.register(r'trajets', TrajetViewSet, basename='trajet')
router.register(r'places', PlaceViewSet, basename='place')
router.register(r'reservations', ReservationViewSet, basename='reservation')

app_name = 'transport'

urlpatterns = [
    path('', include(router.urls)),
]