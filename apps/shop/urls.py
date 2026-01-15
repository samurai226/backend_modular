"""
URLs Shop
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategorieViewSet, ProduitViewSet, PanierViewSet,
    CommandeViewSet, AvisViewSet
)

router = DefaultRouter()
router.register(r'categories', CategorieViewSet, basename='categorie')
router.register(r'produits', ProduitViewSet, basename='produit')
router.register(r'panier', PanierViewSet, basename='panier')
router.register(r'commandes', CommandeViewSet, basename='commande')
router.register(r'avis', AvisViewSet, basename='avis')

app_name = 'shop'

urlpatterns = [
    path('', include(router.urls)),
]