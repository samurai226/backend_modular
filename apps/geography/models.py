"""
Modèles géographiques
"""
from django.db import models
from core.models import BaseModel


class Pays(BaseModel):
    """Modèle représentant un pays"""
    
    nom = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text="Code ISO (BF, FR, CI)")
    indicatif = models.CharField(max_length=10, help_text="Indicatif téléphonique (+226)")
    
    class Meta:
        db_table = 'geography_pays'
        verbose_name = 'Pays'
        verbose_name_plural = 'Pays'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Ville(BaseModel):
    """Modèle représentant une ville"""
    
    nom = models.CharField(max_length=100)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='villes')
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    population = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'geography_ville'
        verbose_name = 'Ville'
        verbose_name_plural = 'Villes'
        ordering = ['nom']
        unique_together = [['nom', 'pays']]
    
    def __str__(self):
        return f"{self.nom} ({self.pays.code})"


class Quartier(BaseModel):
    """Modèle représentant un quartier"""
    
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name='quartiers')
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'geography_quartier'
        verbose_name = 'Quartier'
        verbose_name_plural = 'Quartiers'
        ordering = ['nom']
        unique_together = [['nom', 'ville']]
    
    def __str__(self):
        return f"{self.nom} - {self.ville.nom}"


class Gare(BaseModel):
    """Modèle représentant une gare routière"""
    
    nom = models.CharField(max_length=200)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name='gares')
    quartier = models.ForeignKey(Quartier, on_delete=models.SET_NULL, null=True, blank=True, related_name='gares')
    adresse = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'geography_gare'
        verbose_name = 'Gare'
        verbose_name_plural = 'Gares'
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} - {self.ville.nom}"