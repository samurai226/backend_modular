"""
Serializers Payment
"""
from rest_framework import serializers
from .models import Wallet, Transaction, Paiement, DemandeTransfert


class WalletSerializer(serializers.ModelSerializer):
    """Serializer pour les portefeuilles"""
    user_nom = serializers.CharField(source='user.nom_complet', read_only=True)
    
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ['user', 'solde']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer pour les transactions"""
    user_nom = serializers.CharField(source='user.nom_complet', read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user', 'solde_avant', 'solde_apres']


class PaiementSerializer(serializers.ModelSerializer):
    """Serializer pour les paiements"""
    user_nom = serializers.CharField(source='user.nom_complet', read_only=True)
    
    class Meta:
        model = Paiement
        fields = '__all__'
        read_only_fields = ['user', 'reference_paiement', 'transaction']


class DemandeTransfertSerializer(serializers.ModelSerializer):
    """Serializer pour les transferts"""
    expediteur_nom = serializers.CharField(source='expediteur.nom_complet', read_only=True)
    destinataire_nom = serializers.CharField(source='destinataire.nom_complet', read_only=True)
    
    class Meta:
        model = DemandeTransfert
        fields = '__all__'
        read_only_fields = ['expediteur', 'transaction']