"""
Admin Shop
"""
from django.contrib import admin
from .models import (
    Categorie, Produit, Panier, PanierItem,
    Commande, CommandeItem, Avis
)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'parent', 'is_active', 'ordre']
    list_filter = ['is_active', 'parent']
    search_fields = ['nom']
    prepopulated_fields = {'nom': ('nom',)}


class PanierItemInline(admin.TabularInline):
    model = PanierItem
    extra = 0
    readonly_fields = ['prix_unitaire', 'sous_total']


@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ['user', 'est_actif', 'nombre_items', 'total', 'created_at']
    list_filter = ['est_actif', 'created_at']
    search_fields = ['user__telephone', 'user__nom']
    inlines = [PanierItemInline]
    
    def nombre_items(self, obj):
        return obj.nombre_items
    
    def total(self, obj):
        return f"{obj.total} FCFA"


class CommandeItemInline(admin.TabularInline):
    model = CommandeItem
    extra = 0
    readonly_fields = ['sous_total']


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['numero_commande', 'user', 'total', 'statut', 'est_payee', 'created_at']
    list_filter = ['statut', 'est_payee', 'created_at']
    search_fields = ['numero_commande', 'user__telephone', 'user__nom']
    readonly_fields = ['numero_commande', 'total']
    inlines = [CommandeItemInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Commande', {
            'fields': ('numero_commande', 'user', 'statut')
        }),
        ('Livraison', {
            'fields': ('adresse_livraison', 'ville', 'telephone_livraison', 'notes_livraison')
        }),
        ('Montants', {
            'fields': ('sous_total', 'frais_livraison', 'total')
        }),
        ('Paiement', {
            'fields': ('est_payee', 'methode_paiement', 'paiement')
        }),
        ('Dates', {
            'fields': ('date_confirmation', 'date_expedition', 'date_livraison', 'created_at')
        }),
    )


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'prix', 'prix_promo', 'stock', 'is_active', 'is_featured']
    list_filter = ['categorie', 'is_active', 'is_featured', 'is_new', 'created_at']
    search_fields = ['nom', 'description']
    prepopulated_fields = {'slug': ('nom',)}
    readonly_fields = ['nombre_vues', 'nombre_ventes']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('nom', 'slug', 'categorie', 'description', 'description_courte')
        }),
        ('Prix et Stock', {
            'fields': ('prix', 'prix_promo', 'stock', 'seuil_alerte_stock')
        }),
        ('Images', {
            'fields': ('image_principale', 'image_2', 'image_3', 'image_4')
        }),
        ('Caractéristiques', {
            'fields': ('poids', 'dimensions')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Statut', {
            'fields': ('is_active', 'is_featured', 'is_new')
        }),
        ('Statistiques', {
            'fields': ('nombre_vues', 'nombre_ventes')
        }),
    )


@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ['produit', 'user', 'note', 'is_verified', 'is_visible', 'created_at']
    list_filter = ['note', 'is_verified', 'is_visible', 'created_at']
    search_fields = ['produit__nom', 'user__nom', 'commentaire']
    readonly_fields = ['created_at']