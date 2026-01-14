"""
Modèles d'authentification
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from core.models import BaseModel
from .managers import UserManager


class Role(BaseModel):
    """
    Rôles des utilisateurs
    """
    # Constantes des rôles
    ADMIN = 'admin'
    GERANT = 'gerant'
    GUICHETIER = 'guichetier'
    COLISSIER = 'colissier'
    LIVREUR = 'livreur'
    CLIENT = 'client'
    EXPEDITEUR = 'expediteur'
    RECEPTEUR = 'recepteur'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrateur'),
        (GERANT, 'Gérant de gare'),
        (GUICHETIER, 'Guichetier'),
        (COLISSIER, 'Colissier'),
        (LIVREUR, 'Livreur'),
        (CLIENT, 'Client'),
        (EXPEDITEUR, 'Expéditeur'),
        (RECEPTEUR, 'Récepteur'),
    ]
    
    nom = models.CharField(
        max_length=50, 
        choices=ROLE_CHOICES, 
        unique=True,
        help_text="Code du rôle"
    )
    description = models.TextField(
        help_text="Description du rôle"
    )
    
    class Meta:
        db_table = 'auth_role'
        verbose_name = 'Rôle'
        verbose_name_plural = 'Rôles'
        ordering = ['nom']
    
    def __str__(self):
        return self.get_nom_display()
    
    @property
    def is_admin(self):
        return self.nom == self.ADMIN
    
    @property
    def is_gerant_gare(self):
        return self.nom == self.GERANT
    
    @property
    def is_guichetier(self):
        return self.nom == self.GUICHETIER
    
    @property
    def is_colissier(self):
        return self.nom == self.COLISSIER
    
    @property
    def is_livreur(self):
        return self.nom == self.LIVREUR
    
    @property
    def is_client(self):
        return self.nom == self.CLIENT
    
    @property
    def can_access_mobile(self):
        """Rôles pouvant accéder à l'app mobile"""
        return self.nom in [
            self.LIVREUR, 
            self.GUICHETIER, 
            self.CLIENT, 
            self.EXPEDITEUR, 
            self.RECEPTEUR
        ]


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Modèle utilisateur personnalisé
    Authentification par téléphone
    """
    # Informations personnelles
    nom = models.CharField(max_length=100, help_text="Nom de famille")
    prenom = models.CharField(max_length=100, help_text="Prénom")
    email = models.EmailField(unique=True, null=True, blank=True)
    telephone = models.CharField(max_length=20, unique=True, help_text="Numéro de téléphone")
    
    # Rôle et affectation
    role = models.ForeignKey(
        Role, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='users'
    )
    
    # Statuts
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Informations supplémentaires
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=8, 
        null=True, 
        blank=True,
        help_text="Latitude de localisation"
    )
    longitude = models.DecimalField(
        max_digits=11, 
        decimal_places=8, 
        null=True, 
        blank=True,
        help_text="Longitude de localisation"
    )
    photo_url = models.URLField(max_length=500, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    cnib = models.CharField(max_length=50, null=True, blank=True, help_text="CNIB / Carte d'identité")
    
    # Manager
    objects = UserManager()
    
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['nom', 'prenom']
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['telephone']),
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def nom_complet(self):
        """Nom complet de l'utilisateur"""
        return f"{self.prenom} {self.nom}"
    
    @property
    def nom_complet_inverse(self):
        """Nom complet inversé"""
        return f"{self.nom} {self.prenom}"
    
    # Propriétés pour vérifier les rôles
    @property
    def is_admin(self):
        return self.role and self.role.is_admin
    
    @property
    def is_gerant_gare(self):
        return self.role and self.role.is_gerant_gare
    
    @property
    def is_guichetier(self):
        return self.role and self.role.is_guichetier
    
    @property
    def is_colissier(self):
        return self.role and self.role.is_colissier
    
    @property
    def is_livreur(self):
        return self.role and self.role.is_livreur
    
    @property
    def is_client(self):
        return self.role and self.role.is_client
    
    @property
    def is_expediteur(self):
        return self.role and self.role.nom == Role.EXPEDITEUR
    
    @property
    def is_recepteur(self):
        return self.role and self.role.nom == Role.RECEPTEUR
    
    @property
    def can_access_mobile(self):
        """Peut accéder à l'app mobile"""
        return self.role and self.role.can_access_mobile
    
    @property
    def has_location(self):
        """A une localisation GPS"""
        return self.latitude is not None and self.longitude is not None


class AffectationGare(BaseModel):
    """
    Affectation d'un personnel à une gare
    """
    TYPE_GERANT = 'gerant'
    TYPE_COLISSIER = 'colissier'
    TYPE_GUICHETIER = 'guichetier'
    
    TYPE_CHOICES = [
        (TYPE_GERANT, 'Gérant'),
        (TYPE_COLISSIER, 'Colissier'),
        (TYPE_GUICHETIER, 'Guichetier'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='affectations'
    )
    # Note: gare sera une ForeignKey vers geography.Gare quand l'app sera créée
    # Pour l'instant, on utilise un CharField
    gare_id = models.UUIDField(null=True, blank=True)
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'auth_affectation_gare'
        verbose_name = 'Affectation gare'
        verbose_name_plural = 'Affectations gares'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.nom_complet} - {self.get_type_display()}"
    
    @property
    def is_gerant(self):
        return self.type == self.TYPE_GERANT
    
    @property
    def is_colissier(self):
        return self.type == self.TYPE_COLISSIER
    
    @property
    def is_guichetier(self):
        return self.type == self.TYPE_GUICHETIER
