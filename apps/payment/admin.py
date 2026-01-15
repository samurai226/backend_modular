"""
Admin Payment
"""
from django.contrib import admin
from .models import Wallet, Transaction, Paiement, DemandeTransfert


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'solde', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__telephone', 'user__nom', 'user__prenom']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_transaction', 'montant', 'statut', 'created_at']
    list_filter = ['type_transaction', 'statut', 'created_at']
    search_fields = ['user__telephone', 'reference_externe', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['reference_paiement', 'user', 'type_paiement', 'montant', 'methode_paiement', 'statut', 'created_at']
    list_filter = ['type_paiement', 'methode_paiement', 'statut', 'created_at']
    search_fields = ['reference_paiement', 'user__telephone', 'numero_mobile_money']
    readonly_fields = ['reference_paiement', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(DemandeTransfert)
class DemandeTransfertAdmin(admin.ModelAdmin):
    list_display = ['expediteur', 'destinataire', 'montant', 'statut', 'created_at']
    list_filter = ['statut', 'created_at']
    search_fields = ['expediteur__telephone', 'destinataire__telephone']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'