"""
Modèles Shop (E-commerce)
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import BaseModel
from decimal import Decimal


class Categorie(BaseModel):
    """Catégorie de produits"""
    
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(max_length=500, null=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sous_categories'
    )
    is_active = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'shop_categorie'
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom


class Produit(BaseModel):
    """Produit en vente"""
    
    nom = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    description_courte = models.CharField(max_length=255, null=True, blank=True)
    
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name='produits'
    )
    
    # Prix
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    prix_promo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Stock
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    seuil_alerte_stock = models.IntegerField(default=5)
    
    # Images
    image_principale = models.URLField(max_length=500)
    image_2 = models.URLField(max_length=500, null=True, blank=True)
    image_3 = models.URLField(max_length=500, null=True, blank=True)
    image_4 = models.URLField(max_length=500, null=True, blank=True)
    
    # Caractéristiques
    poids = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Poids en kg"
    )
    dimensions = models.CharField(max_length=100, null=True, blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    
    # Statut
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    
    # Stats
    nombre_vues = models.IntegerField(default=0)
    nombre_ventes = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'shop_produit'
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.nom
    
    @property
    def prix_final(self):
        """Prix final (avec promo si disponible)"""
        if self.prix_promo:
            return self.prix_promo
        return self.prix
    
    @property
    def en_stock(self):
        """Produit en stock"""
        return self.stock > 0
    
    @property
    def stock_faible(self):
        """Stock faible"""
        return self.stock <= self.seuil_alerte_stock
    
    @property
    def pourcentage_reduction(self):
        """Pourcentage de réduction"""
        if self.prix_promo:
            return int(((self.prix - self.prix_promo) / self.prix) * 100)
        return 0
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Panier(BaseModel):
    """Panier d'achat"""
    
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='paniers'
    )
    
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'shop_panier'
        verbose_name = 'Panier'
        verbose_name_plural = 'Paniers'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Panier - {self.user.nom_complet}"
    
    @property
    def total(self):
        """Total du panier"""
        return sum(item.sous_total for item in self.items.all())
    
    @property
    def nombre_items(self):
        """Nombre d'items dans le panier"""
        return sum(item.quantite for item in self.items.all())


class PanierItem(BaseModel):
    """Item dans le panier"""
    
    panier = models.ForeignKey(
        Panier,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='panier_items'
    )
    
    quantite = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    class Meta:
        db_table = 'shop_panier_item'
        verbose_name = 'Item Panier'
        verbose_name_plural = 'Items Panier'
        unique_together = [['panier', 'produit']]
    
    def __str__(self):
        return f"{self.produit.nom} x{self.quantite}"
    
    @property
    def sous_total(self):
        """Sous-total de l'item"""
        return self.prix_unitaire * self.quantite
    
    def save(self, *args, **kwargs):
        # Enregistrer le prix au moment de l'ajout
        if not self.prix_unitaire:
            self.prix_unitaire = self.produit.prix_final
        super().save(*args, **kwargs)


class Commande(BaseModel):
    """Commande client"""
    
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='commandes'
    )
    
    # Numéro de commande
    numero_commande = models.CharField(max_length=20, unique=True)
    
    # Livraison
    adresse_livraison = models.TextField()
    ville = models.ForeignKey(
        'geography.Ville',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    telephone_livraison = models.CharField(max_length=20)
    notes_livraison = models.TextField(null=True, blank=True)
    
    # Montants
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)
    frais_livraison = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Paiement
    est_payee = models.BooleanField(default=False)
    methode_paiement = models.CharField(max_length=20, null=True, blank=True)
    
    paiement = models.ForeignKey(
        'payment.Paiement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commandes'
    )
    
    # Statut
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('en_preparation', 'En préparation'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    # Dates
    date_confirmation = models.DateTimeField(null=True, blank=True)
    date_expedition = models.DateTimeField(null=True, blank=True)
    date_livraison = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'shop_commande'
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.numero_commande} - {self.user.nom_complet}"
    
    def save(self, *args, **kwargs):
        if not self.numero_commande:
            import random
            import string
            self.numero_commande = 'CMD-' + ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
        
        # Calculer le total
        self.total = self.sous_total + self.frais_livraison
        
        super().save(*args, **kwargs)


class CommandeItem(BaseModel):
    """Item dans une commande"""
    
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    produit = models.ForeignKey(
        Produit,
        on_delete=models.SET_NULL,
        null=True,
        related_name='commande_items'
    )
    
    nom_produit = models.CharField(max_length=200)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'shop_commande_item'
        verbose_name = 'Item Commande'
        verbose_name_plural = 'Items Commande'
    
    def __str__(self):
        return f"{self.nom_produit} x{self.quantite}"
    
    @property
    def sous_total(self):
        return self.prix_unitaire * self.quantite


class Avis(BaseModel):
    """Avis sur un produit"""
    
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='avis'
    )
    
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='avis'
    )
    
    note = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    commentaire = models.TextField()
    
    is_verified = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'shop_avis'
        verbose_name = 'Avis'
        verbose_name_plural = 'Avis'
        ordering = ['-created_at']
        unique_together = [['produit', 'user']]
    
    def __str__(self):
        return f"{self.produit.nom} - {self.note}/5 - {self.user.nom_complet}"