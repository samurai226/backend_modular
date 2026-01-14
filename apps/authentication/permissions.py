"""
Permissions personnalisées pour l'app Authentication
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Permission pour les administrateurs uniquement"""
    
    message = "Seuls les administrateurs peuvent effectuer cette action"
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_admin
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """Permission pour le propriétaire de l'objet ou un admin"""
    
    message = "Vous n'avez pas la permission d'effectuer cette action"
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin a tous les droits
        if request.user.is_admin:
            return True
        
        # Propriétaire de l'objet
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'id'):
            return obj.id == request.user.id
        
        return False


class IsGerantGare(permissions.BasePermission):
    """Permission pour les gérants de gare"""
    
    message = "Seuls les gérants de gare peuvent effectuer cette action"
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_gerant_gare
        )


class IsGuichetier(permissions.BasePermission):
    """Permission pour les guichetiers"""
    
    message = "Seuls les guichetiers peuvent effectuer cette action"
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_guichetier
        )


class IsColissier(permissions.BasePermission):
    """Permission pour les colissiers"""
    
    message = "Seuls les colissiers peuvent effectuer cette action"
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_colissier
        )


class IsLivreur(permissions.BasePermission):
    """Permission pour les livreurs"""
    
    message = "Seuls les livreurs peuvent effectuer cette action"
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_livreur
        )


class IsClient(permissions.BasePermission):
    """Permission pour les clients"""
    
    message = "Seuls les clients peuvent effectuer cette action"
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_client
        )
