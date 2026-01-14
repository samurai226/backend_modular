"""
Views pour l'app Authentication
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from .models import Role, User, AffectationGare
from .serializers import (
    RoleSerializer, UserSerializer, RegisterSerializer,
    LoginSerializer, ChangePasswordSerializer, AffectationGareSerializer
)
from .permissions import IsAdmin, IsOwnerOrAdmin


class AuthViewSet(viewsets.GenericViewSet):
    """
    ViewSet pour l'authentification
    Endpoints: register, login, logout, change_password
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Inscription d'un nouvel utilisateur
        POST /api/auth/register/
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'message': 'Inscription réussie'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Connexion utilisateur
        POST /api/auth/login/
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Mettre à jour last_login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'message': 'Connexion réussie'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        Déconnexion utilisateur
        POST /api/auth/logout/
        """
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({
                'message': 'Déconnexion réussie'
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        Changer le mot de passe
        POST /api/auth/change-password/
        """
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            # Vérifier l'ancien mot de passe
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'error': 'Ancien mot de passe incorrect'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Définir le nouveau mot de passe
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Mot de passe modifié avec succès'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les rôles (lecture seule)
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'description']
    ordering_fields = ['nom']


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs
    """
    queryset = User.objects.select_related('role').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['nom', 'prenom', 'telephone', 'email']
    ordering_fields = ['created_at', 'nom', 'prenom']
    
    def get_permissions(self):
        """Permissions selon l'action"""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        elif self.action == 'create':
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Obtenir les informations de l'utilisateur connecté
        GET /api/auth/users/me/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def activate(self, request, pk=None):
        """
        Activer un utilisateur
        POST /api/auth/users/{id}/activate/
        """
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({
            'message': f'Utilisateur {user.nom_complet} activé'
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def deactivate(self, request, pk=None):
        """
        Désactiver un utilisateur
        POST /api/auth/users/{id}/deactivate/
        """
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({
            'message': f'Utilisateur {user.nom_complet} désactivé'
        })


class AffectationGareViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les affectations de gares
    """
    queryset = AffectationGare.objects.select_related('user').all()
    serializer_class = AffectationGareSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'type', 'is_active']
    search_fields = ['user__nom', 'user__prenom']
