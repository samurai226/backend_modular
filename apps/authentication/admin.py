"""
Admin pour l'app Authentication
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Role, User, AffectationGare


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin pour les rôles"""
    list_display = ['nom', 'description', 'created_at']
    search_fields = ['nom', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['nom']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin pour les utilisateurs"""
    list_display = [
        'telephone', 'nom', 'prenom', 'email', 
        'role', 'is_active', 'is_staff', 'created_at'
    ]
    list_filter = ['role', 'is_active', 'is_staff', 'created_at']
    search_fields = ['telephone', 'nom', 'prenom', 'email']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {
            'fields': ('telephone', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'email', 'cnib', 'adresse', 'photo_url')
        }),
        ('Rôle', {
            'fields': ('role',)
        }),
        ('Localisation', {
            'fields': ('latitude', 'longitude')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'created_at', 'updated_at')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'telephone', 'nom', 'prenom', 'email', 
                'password1', 'password2', 'role'
            ),
        }),
    )
    
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login']


@admin.register(AffectationGare)
class AffectationGareAdmin(admin.ModelAdmin):
    """Admin pour les affectations de gares"""
    list_display = [
        'user', 'type', 'is_active', 
        'date_debut', 'date_fin', 'created_at'
    ]
    list_filter = ['type', 'is_active', 'created_at']
    search_fields = ['user__nom', 'user__prenom', 'user__telephone']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Affectation', {
            'fields': ('user', 'gare_id', 'type')
        }),
        ('Période', {
            'fields': ('is_active', 'date_debut', 'date_fin')
        }),
        ('Commentaire', {
            'fields': ('commentaire',)
        }),
        ('Métadonnées', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )
