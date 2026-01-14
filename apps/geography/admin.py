"""
Admin Geography
"""
from django.contrib import admin
from .models import Pays, Ville, Quartier, Gare


@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'indicatif']
    search_fields = ['nom', 'code']


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'pays', 'population']
    list_filter = ['pays']
    search_fields = ['nom']


@admin.register(Quartier)
class QuartierAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville']
    list_filter = ['ville']
    search_fields = ['nom']


@admin.register(Gare)
class GareAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville', 'is_active']
    list_filter = ['ville', 'is_active']
    search_fields = ['nom']