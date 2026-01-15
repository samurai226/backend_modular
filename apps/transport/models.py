"""
Modèles Transport
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import BaseModel


class Compagnie(BaseModel):
    """Compagnie de transport"""
    
    nom = models.CharField(max_length=200, unique=True)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='compagnies/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'transport_compagnie'
        verbose_name = 'Compagnie'
        verbose_name_plural = 'Compagnies'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Bus(BaseModel):
    """Bus/Véhicule"""
    
    compagnie = models.ForeignKey(
        Compagnie,
        on_delete=models.CASCADE,
        related_name='bus'
    )
    numero = models.CharField(max_length=50, unique=True, help_text="Immatriculation")
    modele = models.CharField(max_length=100, null=True, blank=True)
    nombre_places = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'transport_bus'
        verbose_name = 'Bus'
        verbose_name_plural = 'Bus'
        ordering = ['numero']
    
    def __str__(self):
        return f"{self.numero} - {self.compagnie.nom}"


class Trajet(BaseModel):
    """Trajet entre deux gares"""
    
    gare_depart = models.ForeignKey(
        'geography.Gare',
        on_delete=models.CASCADE,
        related_name='trajets_depart'
    )
    gare_arrivee = models.ForeignKey(
        'geography.Gare',
        on_delete=models.CASCADE,
        related_name='trajets_arrivee'
    )
    compagnie = models.ForeignKey(
        Compagnie,
        on_delete=models.CASCADE,
        related_name='trajets'
    )
    bus = models.ForeignKey(
        Bus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trajets'
    )
    
    # Horaires
    heure_depart = models.TimeField()
    heure_arrivee_estimee = models.TimeField()
    date_depart = models.DateField()
    
    # Tarification
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Places
    places_disponibles = models.IntegerField()
    
    # Statut
    STATUT_CHOICES = [
        ('prevu', 'Prévu'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='prevu')
    
    class Meta:
        db_table = 'transport_trajet'
        verbose_name = 'Trajet'
        verbose_name_plural = 'Trajets'
        ordering = ['-date_depart', 'heure_depart']
    
    def __str__(self):
        return f"{self.gare_depart.ville.nom} → {self.gare_arrivee.ville.nom} ({self.date_depart})"
    
    @property
    def places_reservees(self):
        return self.reservations.filter(statut='confirmee').count()


class Place(BaseModel):
    """Place dans un bus pour un trajet"""
    
    trajet = models.ForeignKey(
        Trajet,
        on_delete=models.CASCADE,
        related_name='places'
    )
    numero_place = models.CharField(max_length=10)
    
    STATUT_CHOICES = [
        ('libre', 'Libre'),
        ('reservee', 'Réservée'),
        ('occupee', 'Occupée'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='libre')
    
    class Meta:
        db_table = 'transport_place'
        verbose_name = 'Place'
        verbose_name_plural = 'Places'
        unique_together = [['trajet', 'numero_place']]
        ordering = ['numero_place']
    
    def __str__(self):
        return f"Place {self.numero_place} - {self.trajet}"


class Reservation(BaseModel):
    """Réservation d'un trajet"""
    
    trajet = models.ForeignKey(
        Trajet,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    client = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservations'
    )
    
    # Passager
    nom_passager = models.CharField(max_length=100)
    prenom_passager = models.CharField(max_length=100)
    telephone_passager = models.CharField(max_length=20)
    
    # Prix et paiement
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    est_paye = models.BooleanField(default=False)
    
    # Statut
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
        ('terminee', 'Terminée'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    # Code de réservation
    code_reservation = models.CharField(max_length=20, unique=True)
    
    class Meta:
        db_table = 'transport_reservation'
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code_reservation} - {self.nom_passager}"
    
    def save(self, *args, **kwargs):
        if not self.code_reservation:
            import random
            import string
            self.code_reservation = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)