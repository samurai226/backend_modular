"""
Modèles Delivery (Colis)
"""
from django.db import models
from django.core.validators import MinValueValidator
from core.models import BaseModel
import qrcode
from io import BytesIO
from django.core.files import File


class Colis(BaseModel):
    """Colis à livrer"""
    
    # Expéditeur
    expediteur = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='colis_expedies'
    )
    nom_expediteur = models.CharField(max_length=100)
    telephone_expediteur = models.CharField(max_length=20)
    
    # Destinataire
    destinataire = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='colis_recus'
    )
    nom_destinataire = models.CharField(max_length=100)
    telephone_destinataire = models.CharField(max_length=20)
    adresse_destinataire = models.TextField()
    
    # Trajet
    trajet = models.ForeignKey(
        'transport.Trajet',
        on_delete=models.CASCADE,
        related_name='colis'
    )
    
    # Gares
    gare_depart = models.ForeignKey(
        'geography.Gare',
        on_delete=models.CASCADE,
        related_name='colis_depart'
    )
    gare_arrivee = models.ForeignKey(
        'geography.Gare',
        on_delete=models.CASCADE,
        related_name='colis_arrivee'
    )
    
    # Description du colis
    description = models.TextField()
    poids = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
        help_text="Poids en kg"
    )
    
    TYPE_CHOICES = [
        ('document', 'Document'),
        ('vetement', 'Vêtement'),
        ('nourriture', 'Nourriture'),
        ('electronique', 'Électronique'),
        ('autre', 'Autre'),
    ]
    type_colis = models.CharField(max_length=20, choices=TYPE_CHOICES, default='autre')
    
    # Prix
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    est_paye = models.BooleanField(default=False)
    
    # Statut
    STATUT_CHOICES = [
        ('enregistre', 'Enregistré'),
        ('en_transit', 'En transit'),
        ('arrive', 'Arrivé'),
        ('livre', 'Livré'),
        ('annule', 'Annulé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='enregistre')
    
    # Code de suivi
    code_suivi = models.CharField(max_length=20, unique=True)
    
    # QR Code
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    
    class Meta:
        db_table = 'delivery_colis'
        verbose_name = 'Colis'
        verbose_name_plural = 'Colis'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code_suivi} - {self.nom_destinataire}"
    
    def save(self, *args, **kwargs):
        # Générer le code de suivi
        if not self.code_suivi:
            import random
            import string
            self.code_suivi = 'COL-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        super().save(*args, **kwargs)
        
        # Générer le QR code
        if not self.qr_code:
            self.generate_qr_code()
    
    def generate_qr_code(self):
        """Générer le QR code du colis"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.code_suivi)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        
        self.qr_code.save(f'{self.code_suivi}.png', File(buffer), save=False)
        super().save(update_fields=['qr_code'])


class Livraison(BaseModel):
    """Livraison d'un colis"""
    
    colis = models.OneToOneField(
        Colis,
        on_delete=models.CASCADE,
        related_name='livraison'
    )
    
    livreur = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='livraisons'
    )
    
    date_recuperation = models.DateTimeField(null=True, blank=True)
    date_livraison = models.DateTimeField(null=True, blank=True)
    
    signature_destinataire = models.ImageField(
        upload_to='signatures/',
        null=True,
        blank=True
    )
    
    commentaire = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'delivery_livraison'
        verbose_name = 'Livraison'
        verbose_name_plural = 'Livraisons'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Livraison - {self.colis.code_suivi}"


class HistoriqueEtatColis(BaseModel):
    """Historique des états d'un colis"""
    
    colis = models.ForeignKey(
        Colis,
        on_delete=models.CASCADE,
        related_name='historique'
    )
    
    statut = models.CharField(max_length=20, choices=Colis.STATUT_CHOICES)
    commentaire = models.TextField(null=True, blank=True)
    
    localisation = models.ForeignKey(
        'geography.Gare',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    agent = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'delivery_historique_etat'
        verbose_name = 'Historique État'
        verbose_name_plural = 'Historique États'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.colis.code_suivi} - {self.statut} - {self.created_at}"