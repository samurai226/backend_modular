"""
URLs Payment
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WalletViewSet, TransactionViewSet,
    PaiementViewSet, DemandeTransfertViewSet
)

router = DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallet')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'paiements', PaiementViewSet, basename='paiement')
router.register(r'transferts', DemandeTransfertViewSet, basename='transfert')

app_name = 'payment'

urlpatterns = [
    path('', include(router.urls)),
]