"""
URLs pour l'app Authentication
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import AuthViewSet, RoleViewSet, UserViewSet, AffectationGareViewSet

# Router
router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'users', UserViewSet, basename='user')
router.register(r'affectations', AffectationGareViewSet, basename='affectation')

app_name = 'authentication'

urlpatterns = [
    # Auth endpoints
    path('register/', AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout'),
    path('change-password/', AuthViewSet.as_view({'post': 'change_password'}), name='change_password'),
    
    # Token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Router endpoints
    path('', include(router.urls)),
]
