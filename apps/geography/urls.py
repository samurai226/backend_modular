"""
URLs Geography
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaysViewSet, VilleViewSet, QuartierViewSet, GareViewSet

router = DefaultRouter()
router.register(r'pays', PaysViewSet, basename='pays')
router.register(r'villes', VilleViewSet, basename='ville')
router.register(r'quartiers', QuartierViewSet, basename='quartier')
router.register(r'gares', GareViewSet, basename='gare')

app_name = 'geography'

urlpatterns = [
    path('', include(router.urls)),
]