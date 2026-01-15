"""
Serializers Shop
"""
from rest_framework import serializers
from .models import (
    Categorie, Produit, Panier, PanierItem,
    Commande, CommandeItem, Avis
)


class CategorieSerializer(serializers.ModelSerializer):
    """Serializer pour les catégories"""
    nombre_produits = serializers.IntegerField(source='produits.count', read_only=True)
    sous_categories = serializers.SerializerMethodField()
    
    class Meta:
        model = Categorie
        fields = '__all__'
    
    def get_sous_categories(self, obj):
        if obj.sous_categories.exists():
            return CategorieSerializer(obj.sous_categories.all(), many=True).data
        return []


class AvisSerializer(serializers.ModelSerializer):
    """Serializer pour les avis"""
    user_nom = serializers.CharField(source='user.nom_complet', read_only=True)
    
    class Meta:
        model = Avis
        fields = '__all__'
        read_only_fields = ['user', 'is_verified']


class ProduitListSerializer(serializers.ModelSerializer):
    """Serializer minimal pour la liste de produits"""
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    prix_final = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Produit
        fields = [
            'id', 'nom', 'slug', 'description_courte', 'categorie_nom',
            'prix', 'prix_promo', 'prix_final', 'stock', 'en_stock',
            'image_principale', 'is_featured', 'is_new', 'pourcentage_reduction'
        ]


class ProduitDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour un produit"""
    categorie_detail = CategorieSerializer(source='categorie', read_only=True)
    prix_final = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    pourcentage_reduction = serializers.IntegerField(read_only=True)
    en_stock = serializers.BooleanField(read_only=True)
    stock_faible = serializers.BooleanField(read_only=True)
    avis = AvisSerializer(many=True, read_only=True)
    note_moyenne = serializers.SerializerMethodField()
    nombre_avis = serializers.SerializerMethodField()
    
    class Meta:
        model = Produit
        fields = '__all__'
    
    def get_note_moyenne(self, obj):
        avis = obj.avis.filter(is_visible=True)
        if avis.exists():
            return round(sum(a.note for a in avis) / avis.count(), 1)
        return 0
    
    def get_nombre_avis(self, obj):
        return obj.avis.filter(is_visible=True).count()


class PanierItemSerializer(serializers.ModelSerializer):
    """Serializer pour les items du panier"""
    produit_detail = ProduitListSerializer(source='produit', read_only=True)
    sous_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = PanierItem
        fields = '__all__'
        read_only_fields = ['panier', 'prix_unitaire']


class PanierSerializer(serializers.ModelSerializer):
    """Serializer pour le panier"""
    items = PanierItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    nombre_items = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Panier
        fields = '__all__'
        read_only_fields = ['user']


class CommandeItemSerializer(serializers.ModelSerializer):
    """Serializer pour les items de commande"""
    sous_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CommandeItem
        fields = '__all__'


class CommandeSerializer(serializers.ModelSerializer):
    """Serializer pour les commandes"""
    items = CommandeItemSerializer(many=True, read_only=True)
    user_nom = serializers.CharField(source='user.nom_complet', read_only=True)
    ville_nom = serializers.CharField(source='ville.nom', read_only=True)
    
    class Meta:
        model = Commande
        fields = '__all__'
        read_only_fields = ['user', 'numero_commande', 'total']