"""
Views Payment
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction as db_transaction
from decimal import Decimal

from .models import Wallet, Transaction, Paiement, DemandeTransfert
from .serializers import (
    WalletSerializer, TransactionSerializer,
    PaiementSerializer, DemandeTransfertSerializer
)


class WalletViewSet(viewsets.ModelViewSet):
    """ViewSet pour les portefeuilles"""
    queryset = Wallet.objects.select_related('user').all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrer par user si pas admin"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.is_staff:
            return queryset.filter(user=user)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def mon_wallet(self, request):
        """Wallet de l'utilisateur connecté"""
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(wallet)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def crediter(self, request, pk=None):
        """Créditer un wallet"""
        wallet = self.get_object()
        montant = Decimal(str(request.data.get('montant', 0)))
        
        if montant <= 0:
            return Response(
                {'error': 'Montant invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with db_transaction.atomic():
            solde_avant = wallet.solde
            wallet.crediter(montant)
            
            # Créer transaction
            Transaction.objects.create(
                user=wallet.user,
                type_transaction='depot',
                montant=montant,
                statut='reussie',
                solde_avant=solde_avant,
                solde_apres=wallet.solde,
                description=request.data.get('description', 'Dépôt')
            )
        
        return Response({'message': 'Wallet crédité', 'solde': wallet.solde})


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les transactions (lecture seule)"""
    queryset = Transaction.objects.select_related('user').all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type_transaction', 'statut']
    search_fields = ['reference_externe', 'description']
    
    def get_queryset(self):
        """Transactions de l'utilisateur"""
        return super().get_queryset().filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def historique(self, request):
        """Historique des transactions"""
        transactions = self.get_queryset()[:20]
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)


class PaiementViewSet(viewsets.ModelViewSet):
    """ViewSet pour les paiements"""
    queryset = Paiement.objects.select_related('user', 'transaction').all()
    serializer_class = PaiementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type_paiement', 'statut', 'methode_paiement']
    
    def perform_create(self, serializer):
        """Créer un paiement"""
        paiement = serializer.save(user=self.request.user)
        
        # Si paiement par wallet
        if paiement.methode_paiement == 'wallet':
            self._process_wallet_payment(paiement)
    
    def _process_wallet_payment(self, paiement):
        """Traiter un paiement par wallet"""
        wallet, created = Wallet.objects.get_or_create(user=paiement.user)
        
        with db_transaction.atomic():
            if wallet.debiter(paiement.montant):
                # Transaction réussie
                transaction = Transaction.objects.create(
                    user=paiement.user,
                    type_transaction=f'paiement_{paiement.type_paiement}',
                    montant=paiement.montant,
                    reservation=paiement.reservation,
                    colis=paiement.colis,
                    statut='reussie',
                    solde_avant=wallet.solde + paiement.montant,
                    solde_apres=wallet.solde,
                    description=f'Paiement {paiement.reference_paiement}'
                )
                
                paiement.transaction = transaction
                paiement.statut = 'valide'
                paiement.save()
                
                # Marquer comme payé
                if paiement.reservation:
                    paiement.reservation.est_paye = True
                    paiement.reservation.save()
                elif paiement.colis:
                    paiement.colis.est_paye = True
                    paiement.colis.save()
            else:
                paiement.statut = 'refuse'
                paiement.save()


class DemandeTransfertViewSet(viewsets.ModelViewSet):
    """ViewSet pour les transferts"""
    queryset = DemandeTransfert.objects.select_related(
        'expediteur', 'destinataire', 'transaction'
    ).all()
    serializer_class = DemandeTransfertSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Créer une demande de transfert"""
        serializer.save(expediteur=self.request.user)
    
    @action(detail=True, methods=['post'])
    def accepter(self, request, pk=None):
        """Accepter un transfert"""
        demande = self.get_object()
        
        if demande.destinataire != request.user:
            return Response(
                {'error': 'Vous n\'êtes pas le destinataire'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        wallet_exp, _ = Wallet.objects.get_or_create(user=demande.expediteur)
        wallet_dest, _ = Wallet.objects.get_or_create(user=demande.destinataire)
        
        with db_transaction.atomic():
            if wallet_exp.debiter(demande.montant):
                wallet_dest.crediter(demande.montant)
                
                # Transaction
                transaction = Transaction.objects.create(
                    user=demande.expediteur,
                    type_transaction='transfert_envoye',
                    montant=demande.montant,
                    statut='reussie',
                    solde_avant=wallet_exp.solde + demande.montant,
                    solde_apres=wallet_exp.solde,
                    description=f'Transfert vers {demande.destinataire.nom_complet}'
                )
                
                Transaction.objects.create(
                    user=demande.destinataire,
                    type_transaction='transfert_recu',
                    montant=demande.montant,
                    statut='reussie',
                    solde_avant=wallet_dest.solde - demande.montant,
                    solde_apres=wallet_dest.solde,
                    description=f'Transfert de {demande.expediteur.nom_complet}'
                )
                
                demande.transaction = transaction
                demande.statut = 'accepte'
                demande.save()
                
                return Response({'message': 'Transfert accepté'})
            else:
                return Response(
                    {'error': 'Solde insuffisant'},
                    status=status.HTTP_400_BAD_REQUEST
                )