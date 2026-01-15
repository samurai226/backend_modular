"""
Admin Notifications
"""
from django.contrib import admin
from .models import Notification, NotificationTemplate, NotificationPreference


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'type_notification', 'is_active']
    list_filter = ['type_notification', 'is_active']
    search_fields = ['code', 'nom']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_notification', 'titre', 'is_read', 'is_sent', 'created_at']
    list_filter = ['type_notification', 'is_read', 'is_sent', 'created_at']
    search_fields = ['user__telephone', 'user__nom', 'titre', 'message']
    readonly_fields = ['created_at', 'sent_at', 'read_at']
    date_hierarchy = 'created_at'


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'activer_email', 'activer_sms', 'activer_push', 'activer_in_app']
    search_fields = ['user__telephone', 'user__nom']