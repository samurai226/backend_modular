"""
Views Notifications
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Notification, NotificationTemplate, NotificationPreference
from .serializers import (
    NotificationSerializer, NotificationTemplateSerializer,
    NotificationPreferenceSerializer
)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet pour les templates (admin seulement)"""
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type_notification', 'is_active']
    search_fields = ['code', 'nom']


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet pour les notifications"""
    queryset = Notification.objects.select_related('user', 'template').all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type_notification', 'is_read', 'is_sent']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Notifications de l'utilisateur connecté"""
        return super().get_queryset().filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def non_lues(self, request):
        """Notifications non lues"""
        notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def count_non_lues(self, request):
        """Nombre de notifications non lues"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'count': count})
    
    @action(detail=True, methods=['post'])
    def marquer_lue(self, request, pk=None):
        """Marquer une notification comme lue"""
        notification = self.get_object()
        notification.marquer_lue()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def marquer_toutes_lues(self, request):
        """Marquer toutes les notifications comme lues"""
        notifications = self.get_queryset().filter(is_read=False)
        notifications.update(
            is_read=True,
            read_at=timezone.now()
        )
        return Response({'message': f'{notifications.count()} notifications marquées comme lues'})
    
    @action(detail=False, methods=['delete'])
    def supprimer_lues(self, request):
        """Supprimer toutes les notifications lues"""
        count = self.get_queryset().filter(is_read=True).delete()[0]
        return Response({'message': f'{count} notifications supprimées'})


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet pour les préférences"""
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def mes_preferences(self, request):
        """Préférences de l'utilisateur connecté"""
        preference, created = NotificationPreference.objects.get_or_create(
            user=request.user
        )
        serializer = self.get_serializer(preference)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def modifier(self, request):
        """Modifier les préférences"""
        preference, created = NotificationPreference.objects.get_or_create(
            user=request.user
        )
        serializer = self.get_serializer(preference, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)