"""
URLs Delivery
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ColisViewSet, LivraisonViewSet, HistoriqueEtatColisViewSet

router = DefaultRouter()
router.register(r'colis', ColisViewSet, basename='colis')
router.register(r'livraisons', LivraisonViewSet, basename='livraison')
router.register(r'historique', HistoriqueEtatColisViewSet, basename='historique')

app_name = 'delivery'

urlpatterns = [
    path('', include(router.urls)),
]