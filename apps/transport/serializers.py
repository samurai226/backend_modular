"""
Serializers Transport
"""
from rest_framework import serializers
from .models import Compagnie, Bus, Trajet, Place, Reservation
from apps.geography.serializers import GareSerializer


class CompagnieSerializer(serializers.ModelSerializer):
    """Serializer pour les compagnies"""
    nombre_bus = serializers.IntegerField(source='bus.count', read_only=True)
    
    class Meta:
        model = Compagnie
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    """Serializer pour les bus"""
    compagnie_detail = CompagnieSerializer(source='compagnie', read_only=True)
    
    class Meta:
        model = Bus
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer pour les places"""
    
    class Meta:
        model = Place
        fields = '__all__'


class TrajetSerializer(serializers.ModelSerializer):
    """Serializer pour les trajets"""
    gare_depart_detail = GareSerializer(source='gare_depart', read_only=True)
    gare_arrivee_detail = GareSerializer(source='gare_arrivee', read_only=True)
    compagnie_detail = CompagnieSerializer(source='compagnie', read_only=True)
    bus_detail = BusSerializer(source='bus', read_only=True)
    places_reservees = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Trajet
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer pour les réservations"""
    trajet_detail = TrajetSerializer(source='trajet', read_only=True)
    client_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['code_reservation', 'client']
    
    def get_client_detail(self, obj):
        return {
            'id': obj.client.id,
            'nom_complet': obj.client.nom_complet,
            'telephone': obj.client.telephone,
        }