"""
Serializers Notifications
"""
from rest_framework import serializers
from .models import Notification, NotificationTemplate, NotificationPreference


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """Serializer pour les templates"""
    
    class Meta:
        model = NotificationTemplate
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer pour les notifications"""
    user_nom = serializers.CharField(source='user.nom_complet', read_only=True)
    template_nom = serializers.CharField(source='template.nom', read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user', 'is_sent', 'sent_at', 'error_message']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer pour les préférences"""
    
    class Meta:
        model = NotificationPreference
        fields = '__all__'
        read_only_fields = ['user']