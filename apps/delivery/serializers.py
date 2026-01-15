"""
Serializers Delivery
"""
from rest_framework import serializers
from .models import Colis, Livraison, HistoriqueEtatColis


class HistoriqueEtatColisSerializer(serializers.ModelSerializer):
    """Serializer pour l'historique"""
    agent_nom = serializers.CharField(source='agent.nom_complet', read_only=True)
    localisation_nom = serializers.CharField(source='localisation.nom', read_only=True)
    
    class Meta:
        model = HistoriqueEtatColis
        fields = '__all__'


class LivraisonSerializer(serializers.ModelSerializer):
    """Serializer pour les livraisons"""
    livreur_nom = serializers.CharField(source='livreur.nom_complet', read_only=True)
    
    class Meta:
        model = Livraison
        fields = '__all__'


class ColisSerializer(serializers.ModelSerializer):
    """Serializer pour les colis"""
    expediteur_detail = serializers.SerializerMethodField()
    destinataire_detail = serializers.SerializerMethodField()
    gare_depart_nom = serializers.CharField(source='gare_depart.nom', read_only=True)
    gare_arrivee_nom = serializers.CharField(source='gare_arrivee.nom', read_only=True)
    trajet_info = serializers.SerializerMethodField()
    livraison = LivraisonSerializer(read_only=True)
    historique = HistoriqueEtatColisSerializer(many=True, read_only=True)
    
    class Meta:
        model = Colis
        fields = '__all__'
        read_only_fields = ['code_suivi', 'qr_code', 'expediteur']
    
    def get_expediteur_detail(self, obj):
        return {
            'nom': obj.nom_expediteur,
            'telephone': obj.telephone_expediteur,
        }
    
    def get_destinataire_detail(self, obj):
        return {
            'nom': obj.nom_destinataire,
            'telephone': obj.telephone_destinataire,
            'adresse': obj.adresse_destinataire,
        }
    
    def get_trajet_info(self, obj):
        return {
            'depart': obj.trajet.gare_depart.ville.nom,
            'arrivee': obj.trajet.gare_arrivee.ville.nom,
            'date': obj.trajet.date_depart,
        }


class ColisMinimalSerializer(serializers.ModelSerializer):
    """Serializer minimal pour les listes"""
    
    class Meta:
        model = Colis
        fields = ['id', 'code_suivi', 'nom_destinataire', 'statut', 'est_paye']