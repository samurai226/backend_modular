"""
Views Delivery
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Colis, Livraison, HistoriqueEtatColis
from .serializers import (
    ColisSerializer, ColisMinimalSerializer,
    LivraisonSerializer, HistoriqueEtatColisSerializer
)


class ColisViewSet(viewsets.ModelViewSet):
    """ViewSet pour les colis"""
    queryset = Colis.objects.select_related(
        'expediteur', 'destinataire', 'trajet', 'gare_depart', 'gare_arrivee'
    ).prefetch_related('historique').all()
    serializer_class = ColisSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['statut', 'gare_depart', 'gare_arrivee', 'trajet', 'est_paye']
    search_fields = ['code_suivi', 'nom_destinataire', 'telephone_destinataire']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ColisMinimalSerializer
        return ColisSerializer
    
    def perform_create(self, serializer):
        """Associer l'expéditeur connecté"""
        colis = serializer.save(expediteur=self.request.user)
        
        # Créer le premier historique
        HistoriqueEtatColis.objects.create(
            colis=colis,
            statut='enregistre',
            commentaire='Colis enregistré',
            localisation=colis.gare_depart,
            agent=self.request.user
        )
    
    @action(detail=False, methods=['get'])
    def mes_colis(self, request):
        """Colis de l'utilisateur connecté"""
        colis = self.get_queryset().filter(expediteur=request.user)
        serializer = self.get_serializer(colis, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def suivre(self, request, pk=None):
        """Suivre un colis par son code"""
        colis = self.get_object()
        serializer = self.get_serializer(colis)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def suivre_code(self, request):
        """Suivre un colis par code de suivi"""
        code_suivi = request.data.get('code_suivi')
        
        try:
            colis = Colis.objects.get(code_suivi=code_suivi)
            serializer = self.get_serializer(colis)
            return Response(serializer.data)
        except Colis.DoesNotExist:
            return Response(
                {'error': 'Colis non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def changer_statut(self, request, pk=None):
        """Changer le statut d'un colis"""
        colis = self.get_object()
        nouveau_statut = request.data.get('statut')
        commentaire = request.data.get('commentaire', '')
        
        if nouveau_statut not in dict(Colis.STATUT_CHOICES):
            return Response(
                {'error': 'Statut invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        colis.statut = nouveau_statut
        colis.save()
        
        # Ajouter à l'historique
        HistoriqueEtatColis.objects.create(
            colis=colis,
            statut=nouveau_statut,
            commentaire=commentaire,
            agent=request.user
        )
        
        return Response({'message': 'Statut mis à jour'})


class LivraisonViewSet(viewsets.ModelViewSet):
    """ViewSet pour les livraisons"""
    queryset = Livraison.objects.select_related('colis', 'livreur').all()
    serializer_class = LivraisonSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['livreur', 'colis']
    
    @action(detail=True, methods=['post'])
    def confirmer_livraison(self, request, pk=None):
        """Confirmer la livraison"""
        livraison = self.get_object()
        livraison.date_livraison = timezone.now()
        livraison.save()
        
        # Mettre à jour le statut du colis
        colis = livraison.colis
        colis.statut = 'livre'
        colis.save()
        
        # Historique
        HistoriqueEtatColis.objects.create(
            colis=colis,
            statut='livre',
            commentaire='Colis livré au destinataire',
            agent=request.user
        )
        
        return Response({'message': 'Livraison confirmée'})


class HistoriqueEtatColisViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour l'historique (lecture seule)"""
    queryset = HistoriqueEtatColis.objects.select_related('colis', 'agent', 'localisation').all()
    serializer_class = HistoriqueEtatColisSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['colis', 'statut']