"""
Admin Delivery
"""
from django.contrib import admin
from .models import Colis, Livraison, HistoriqueEtatColis


@admin.register(Colis)
class ColisAdmin(admin.ModelAdmin):
    list_display = ['code_suivi', 'nom_destinataire', 'statut', 'gare_depart', 'gare_arrivee', 'est_paye']
    list_filter = ['statut', 'est_paye', 'type_colis', 'created_at']
    search_fields = ['code_suivi', 'nom_destinataire', 'telephone_destinataire']
    readonly_fields = ['code_suivi', 'qr_code']
    date_hierarchy = 'created_at'


@admin.register(Livraison)
class LivraisonAdmin(admin.ModelAdmin):
    list_display = ['colis', 'livreur', 'date_recuperation', 'date_livraison']
    list_filter = ['date_recuperation', 'date_livraison']
    search_fields = ['colis__code_suivi']


@admin.register(HistoriqueEtatColis)
class HistoriqueEtatColisAdmin(admin.ModelAdmin):
    list_display = ['colis', 'statut', 'localisation', 'agent', 'created_at']
    list_filter = ['statut', 'created_at']
    search_fields = ['colis__code_suivi']