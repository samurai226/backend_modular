"""
Modèles Payment
"""
from django.db import models
from django.core.validators import MinValueValidator
from core.models import BaseModel
from decimal import Decimal


class Wallet(BaseModel):
    """Portefeuille utilisateur"""
    
    user = models.OneToOneField(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    
    solde = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'payment_wallet'
        verbose_name = 'Portefeuille'
        verbose_name_plural = 'Portefeuilles'
    
    def __str__(self):
        return f"Wallet - {self.user.nom_complet} ({self.solde} FCFA)"
    
    def crediter(self, montant):
        """Créditer le portefeuille"""
        self.solde += Decimal(str(montant))
        self.save()
    
    def debiter(self, montant):
        """Débiter le portefeuille"""
        montant = Decimal(str(montant))
        if self.solde >= montant:
            self.solde -= montant
            self.save()
            return True
        return False


class Transaction(BaseModel):
    """Transaction financière"""
    
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    
    TYPE_CHOICES = [
        ('depot', 'Dépôt'),
        ('retrait', 'Retrait'),
        ('paiement_reservation', 'Paiement Réservation'),
        ('paiement_colis', 'Paiement Colis'),
        ('remboursement', 'Remboursement'),
        ('transfert_envoye', 'Transfert Envoyé'),
        ('transfert_recu', 'Transfert Reçu'),
    ]
    type_transaction = models.CharField(max_length=30, choices=TYPE_CHOICES)
    
    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Références optionnelles
    reservation = models.ForeignKey(
        'transport.Reservation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    
    colis = models.ForeignKey(
        'delivery.Colis',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    
    # Statut
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('reussie', 'Réussie'),
        ('echouee', 'Échouée'),
        ('annulee', 'Annulée'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    # Informations supplémentaires
    reference_externe = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    # Solde après transaction
    solde_avant = models.DecimalField(max_digits=12, decimal_places=2)
    solde_apres = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        db_table = 'payment_transaction'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.type_transaction} - {self.montant} FCFA - {self.user.nom_complet}"


class Paiement(BaseModel):
    """Paiement pour réservation ou colis"""
    
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='paiements'
    )
    
    # Type de paiement
    TYPE_CHOICES = [
        ('reservation', 'Réservation'),
        ('colis', 'Colis'),
    ]
    type_paiement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Référence
    reservation = models.ForeignKey(
        'transport.Reservation',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='paiements'
    )
    
    colis = models.ForeignKey(
        'delivery.Colis',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='paiements'
    )
    
    # Montant
    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Méthode de paiement
    METHODE_CHOICES = [
        ('wallet', 'Portefeuille'),
        ('mobile_money', 'Mobile Money'),
        ('carte_bancaire', 'Carte Bancaire'),
        ('especes', 'Espèces'),
    ]
    methode_paiement = models.CharField(max_length=20, choices=METHODE_CHOICES)
    
    # Statut
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('rembourse', 'Remboursé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    # Transaction associée
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paiement'
    )
    
    # Informations mobile money
    numero_mobile_money = models.CharField(max_length=20, null=True, blank=True)
    operateur_mobile_money = models.CharField(max_length=50, null=True, blank=True)
    
    # Référence
    reference_paiement = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'payment_paiement'
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reference_paiement} - {self.montant} FCFA"
    
    def save(self, *args, **kwargs):
        if not self.reference_paiement:
            import random
            import string
            self.reference_paiement = 'PAY-' + ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=10)
            )
        super().save(*args, **kwargs)


class DemandeTransfert(BaseModel):
    """Demande de transfert d'argent entre utilisateurs"""
    
    expediteur = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='transferts_envoyes'
    )
    
    destinataire = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='transferts_recus'
    )
    
    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    motif = models.TextField(null=True, blank=True)
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
        ('annule', 'Annulé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demande_transfert'
    )
    
    class Meta:
        db_table = 'payment_demande_transfert'
        verbose_name = 'Demande de Transfert'
        verbose_name_plural = 'Demandes de Transfert'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.expediteur.nom_complet} → {self.destinataire.nom_complet} ({self.montant} FCFA)"