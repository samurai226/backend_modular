"""
Views Shop
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg
from django.db import transaction as db_transaction

from .models import (
    Categorie, Produit, Panier, PanierItem,
    Commande, CommandeItem, Avis
)
from .serializers import (
    CategorieSerializer, ProduitListSerializer, ProduitDetailSerializer,
    PanierSerializer, PanierItemSerializer, CommandeSerializer,
    CommandeItemSerializer, AvisSerializer
)


class CategorieViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les catégories (lecture seule)"""
    queryset = Categorie.objects.filter(is_active=True)
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]
    
    @action(detail=True, methods=['get'])
    def produits(self, request, pk=None):
        """Produits d'une catégorie"""
        categorie = self.get_object()
        produits = Produit.objects.filter(
            categorie=categorie,
            is_active=True
        )
        serializer = ProduitListSerializer(produits, many=True)
        return Response(serializer.data)


class ProduitViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les produits (lecture seule)"""
    queryset = Produit.objects.filter(is_active=True).select_related('categorie')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorie', 'is_featured', 'is_new']
    search_fields = ['nom', 'description', 'description_courte']
    ordering_fields = ['prix', 'created_at', 'nombre_ventes']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProduitDetailSerializer
        return ProduitListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Incrémenter le nombre de vues"""
        instance = self.get_object()
        instance.nombre_vues += 1
        instance.save(update_fields=['nombre_vues'])
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Produits en vedette"""
        produits = self.get_queryset().filter(is_featured=True)[:10]
        serializer = self.get_serializer(produits, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def nouveautes(self, request):
        """Nouveaux produits"""
        produits = self.get_queryset().filter(is_new=True).order_by('-created_at')[:10]
        serializer = self.get_serializer(produits, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def promotions(self, request):
        """Produits en promotion"""
        produits = self.get_queryset().filter(prix_promo__isnull=False)
        serializer = self.get_serializer(produits, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recherche(self, request):
        """Recherche avancée"""
        query = request.query_params.get('q', '')
        prix_min = request.query_params.get('prix_min')
        prix_max = request.query_params.get('prix_max')
        
        produits = self.get_queryset()
        
        if query:
            produits = produits.filter(
                Q(nom__icontains=query) |
                Q(description__icontains=query) |
                Q(description_courte__icontains=query)
            )
        
        if prix_min:
            produits = produits.filter(prix__gte=prix_min)
        
        if prix_max:
            produits = produits.filter(prix__lte=prix_max)
        
        serializer = self.get_serializer(produits, many=True)
        return Response(serializer.data)


class PanierViewSet(viewsets.ModelViewSet):
    """ViewSet pour le panier"""
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, est_actif=True)
    
    @action(detail=False, methods=['get'])
    def mon_panier(self, request):
        """Panier actif de l'utilisateur"""
        panier, created = Panier.objects.get_or_create(
            user=request.user,
            est_actif=True
        )
        serializer = self.get_serializer(panier)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def ajouter(self, request):
        """Ajouter un produit au panier"""
        produit_id = request.data.get('produit_id')
        quantite = int(request.data.get('quantite', 1))
        
        try:
            produit = Produit.objects.get(id=produit_id, is_active=True)
        except Produit.DoesNotExist:
            return Response(
                {'error': 'Produit non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier le stock
        if produit.stock < quantite:
            return Response(
                {'error': 'Stock insuffisant'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer ou créer le panier
        panier, created = Panier.objects.get_or_create(
            user=request.user,
            est_actif=True
        )
        
        # Ajouter ou mettre à jour l'item
        item, created = PanierItem.objects.get_or_create(
            panier=panier,
            produit=produit,
            defaults={'quantite': quantite, 'prix_unitaire': produit.prix_final}
        )
        
        if not created:
            item.quantite += quantite
            item.save()
        
        serializer = PanierSerializer(panier)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def modifier_quantite(self, request):
        """Modifier la quantité d'un item"""
        item_id = request.data.get('item_id')
        quantite = int(request.data.get('quantite', 1))
        
        try:
            item = PanierItem.objects.get(
                id=item_id,
                panier__user=request.user,
                panier__est_actif=True
            )
        except PanierItem.DoesNotExist:
            return Response(
                {'error': 'Item non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if quantite <= 0:
            item.delete()
        else:
            item.quantite = quantite
            item.save()
        
        serializer = PanierSerializer(item.panier)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def retirer(self, request):
        """Retirer un item du panier"""
        item_id = request.data.get('item_id')
        
        try:
            item = PanierItem.objects.get(
                id=item_id,
                panier__user=request.user,
                panier__est_actif=True
            )
            panier = item.panier
            item.delete()
            
            serializer = PanierSerializer(panier)
            return Response(serializer.data)
        except PanierItem.DoesNotExist:
            return Response(
                {'error': 'Item non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def vider(self, request):
        """Vider le panier"""
        panier = Panier.objects.filter(
            user=request.user,
            est_actif=True
        ).first()
        
        if panier:
            panier.items.all().delete()
            serializer = self.get_serializer(panier)
            return Response(serializer.data)
        
        return Response({'message': 'Panier vide'})


class CommandeViewSet(viewsets.ModelViewSet):
    """ViewSet pour les commandes"""
    queryset = Commande.objects.select_related('user', 'ville').prefetch_related('items').all()
    serializer_class = CommandeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['statut', 'est_payee']
    
    def get_queryset(self):
        """Filtrer par user si pas admin"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.is_staff:
            return queryset.filter(user=user)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def creer_depuis_panier(self, request):
        """Créer une commande depuis le panier"""
        panier = Panier.objects.filter(
            user=request.user,
            est_actif=True
        ).first()
        
        if not panier or not panier.items.exists():
            return Response(
                {'error': 'Panier vide'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with db_transaction.atomic():
            # Créer la commande
            commande = Commande.objects.create(
                user=request.user,
                adresse_livraison=request.data.get('adresse_livraison'),
                ville_id=request.data.get('ville_id'),
                telephone_livraison=request.data.get('telephone_livraison'),
                notes_livraison=request.data.get('notes_livraison', ''),
                sous_total=panier.total,
                frais_livraison=request.data.get('frais_livraison', 0),
                methode_paiement=request.data.get('methode_paiement')
            )
            
            # Créer les items de commande
            for item in panier.items.all():
                CommandeItem.objects.create(
                    commande=commande,
                    produit=item.produit,
                    nom_produit=item.produit.nom,
                    quantite=item.quantite,
                    prix_unitaire=item.prix_unitaire
                )
                
                # Mettre à jour le stock
                item.produit.s

class AvisViewSet(viewsets.ModelViewSet):
    """ViewSet pour les avis"""
    queryset = Avis.objects.select_related('produit', 'user').all()
    serializer_class = AvisSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['produit', 'note', 'is_verified']
    
    def get_queryset(self):
        """Filtrer les avis visibles pour les non-admins"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.is_staff:
            # Les clients voient seulement les avis visibles + leurs propres avis
            return queryset.filter(
                models.Q(is_visible=True) | models.Q(user=user)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        """Associer l'utilisateur connecté"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def mes_avis(self, request):
        """Avis de l'utilisateur connecté"""
        avis = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(avis, many=True)
        return Response(serializer.data)