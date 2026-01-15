"""
Admin Transport
"""
from django.contrib import admin
from .models import Compagnie, Bus, Trajet, Place, Reservation


@admin.register(Compagnie)
class CompagnieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'telephone', 'is_active']
    search_fields = ['nom']
    list_filter = ['is_active']


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['numero', 'compagnie', 'nombre_places', 'is_active']
    list_filter = ['compagnie', 'is_active']
    search_fields = ['numero']


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = ['gare_depart', 'gare_arrivee', 'date_depart', 'heure_depart', 'prix', 'statut']
    list_filter = ['statut', 'compagnie', 'date_depart']
    search_fields = ['gare_depart__nom', 'gare_arrivee__nom']
    date_hierarchy = 'date_depart'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['numero_place', 'trajet', 'statut']
    list_filter = ['statut']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['code_reservation', 'nom_passager', 'trajet', 'statut', 'est_paye', 'created_at']
    list_filter = ['statut', 'est_paye', 'created_at']
    search_fields = ['code_reservation', 'nom_passager', 'telephone_passager']
    readonly_fields = ['code_reservation']