"""
Views Transport
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date

from .models import Compagnie, Bus, Trajet, Place, Reservation
from .serializers import (
    CompagnieSerializer, BusSerializer, TrajetSerializer,
    PlaceSerializer, ReservationSerializer
)


class CompagnieViewSet(viewsets.ModelViewSet):
    """ViewSet pour les compagnies"""
    queryset = Compagnie.objects.all()
    serializer_class = CompagnieSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['nom']


class BusViewSet(viewsets.ModelViewSet):
    """ViewSet pour les bus"""
    queryset = Bus.objects.select_related('compagnie').all()
    serializer_class = BusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['compagnie', 'is_active']
    search_fields = ['numero', 'modele']


class TrajetViewSet(viewsets.ModelViewSet):
    """ViewSet pour les trajets"""
    queryset = Trajet.objects.select_related(
        'gare_depart', 'gare_arrivee', 'compagnie', 'bus'
    ).all()
    serializer_class = TrajetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gare_depart', 'gare_arrivee', 'compagnie', 'statut', 'date_depart']
    search_fields = ['gare_depart__nom', 'gare_arrivee__nom']
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """Trajets disponibles (places libres)"""
        trajets = self.get_queryset().filter(
            statut='prevu',
            date_depart__gte=date.today(),
            places_disponibles__gt=0
        )
        serializer = self.get_serializer(trajets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def places(self, request, pk=None):
        """Places d'un trajet"""
        trajet = self.get_object()
        places = trajet.places.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)


class PlaceViewSet(viewsets.ModelViewSet):
    """ViewSet pour les places"""
    queryset = Place.objects.select_related('trajet').all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['trajet', 'statut']


class ReservationViewSet(viewsets.ModelViewSet):
    """ViewSet pour les réservations"""
    queryset = Reservation.objects.select_related('trajet', 'client', 'place').all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['trajet', 'client', 'statut', 'est_paye']
    search_fields = ['code_reservation', 'nom_passager', 'telephone_passager']
    
    def get_queryset(self):
        """Filtrer par client si pas admin"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.is_staff and user.role and user.role.nom == 'client':
            return queryset.filter(client=user)
        
        return queryset
    
    def perform_create(self, serializer):
        """Associer le client connecté"""
        serializer.save(client=self.request.user)
    
    @action(detail=True, methods=['post'])
    def confirmer(self, request, pk=None):
        """Confirmer une réservation"""
        reservation = self.get_object()
        reservation.statut = 'confirmee'
        reservation.save()
        return Response({'message': 'Réservation confirmée'})
    
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """Annuler une réservation"""
        reservation = self.get_object()
        reservation.statut = 'annulee'
        reservation.save()
        return Response({'message': 'Réservation annulée'})
    
    @action(detail=False, methods=['get'])
    def mes_reservations(self, request):
        """Réservations du client connecté"""
        reservations = self.get_queryset().filter(client=request.user)
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)