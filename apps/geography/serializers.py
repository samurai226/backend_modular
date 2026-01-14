"""
Serializers Geography
"""
from rest_framework import serializers
from .models import Pays, Ville, Quartier, Gare


class PaysSerializer(serializers.ModelSerializer):
    """Serializer pour les pays"""
    
    class Meta:
        model = Pays
        fields = '__all__'


class VilleSerializer(serializers.ModelSerializer):
    """Serializer pour les villes"""
    pays_detail = PaysSerializer(source='pays', read_only=True)
    
    class Meta:
        model = Ville
        fields = '__all__'


class QuartierSerializer(serializers.ModelSerializer):
    """Serializer pour les quartiers"""
    ville_detail = VilleSerializer(source='ville', read_only=True)
    
    class Meta:
        model = Quartier
        fields = '__all__'


class GareSerializer(serializers.ModelSerializer):
    """Serializer pour les gares"""
    ville_detail = VilleSerializer(source='ville', read_only=True)
    quartier_detail = QuartierSerializer(source='quartier', read_only=True)
    
    class Meta:
        model = Gare
        fields = '__all__'