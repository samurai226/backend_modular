"""
Views Geography
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Pays, Ville, Quartier, Gare
from .serializers import PaysSerializer, VilleSerializer, QuartierSerializer, GareSerializer


class PaysViewSet(viewsets.ModelViewSet):
    """ViewSet pour les pays"""
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nom', 'code']


class VilleViewSet(viewsets.ModelViewSet):
    """ViewSet pour les villes"""
    queryset = Ville.objects.select_related('pays').all()
    serializer_class = VilleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['pays']
    search_fields = ['nom']


class QuartierViewSet(viewsets.ModelViewSet):
    """ViewSet pour les quartiers"""
    queryset = Quartier.objects.select_related('ville').all()
    serializer_class = QuartierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ville']
    search_fields = ['nom']


class GareViewSet(viewsets.ModelViewSet):
    """ViewSet pour les gares"""
    queryset = Gare.objects.select_related('ville', 'quartier').all()
    serializer_class = GareSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ville', 'is_active']
    search_fields = ['nom']