"""
Modèles Notifications
"""
from django.db import models
from core.models import BaseModel


class NotificationTemplate(BaseModel):
    """Template de notification"""
    
    code = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=200)
    
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push'),
        ('in_app', 'In-App'),
    ]
    type_notification = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Contenu
    titre = models.CharField(max_length=200, help_text="Supporte les variables: {user}, {montant}, etc.")
    message = models.TextField(help_text="Supporte les variables: {user}, {montant}, etc.")
    
    # Email spécifique
    sujet_email = models.CharField(max_length=200, null=True, blank=True)
    html_email = models.TextField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'notifications_template'
        verbose_name = 'Template Notification'
        verbose_name_plural = 'Templates Notifications'
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.nom}"
    
    def render(self, context):
        """Rendre le template avec les variables"""
        titre = self.titre.format(**context)
        message = self.message.format(**context)
        return titre, message


class Notification(BaseModel):
    """Notification envoyée à un utilisateur"""
    
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push'),
        ('in_app', 'In-App'),
    ]
    type_notification = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Contenu
    titre = models.CharField(max_length=200)
    message = models.TextField()
    
    # Données additionnelles (JSON)
    data = models.JSONField(null=True, blank=True)
    
    # Références optionnelles
    reservation = models.ForeignKey(
        'transport.Reservation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    colis = models.ForeignKey(
        'delivery.Colis',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    commande = models.ForeignKey(
        'shop.Commande',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    # Statut
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Envoi
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'notifications_notification'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.type_notification} - {self.user.nom_complet} - {self.titre}"
    
    def marquer_lue(self):
        """Marquer comme lue"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class NotificationPreference(BaseModel):
    """Préférences de notification d'un utilisateur"""
    
    user = models.OneToOneField(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    
    # Préférences par canal
    activer_email = models.BooleanField(default=True)
    activer_sms = models.BooleanField(default=True)
    activer_push = models.BooleanField(default=True)
    activer_in_app = models.BooleanField(default=True)
    
    # Préférences par type
    notifications_reservations = models.BooleanField(default=True)
    notifications_colis = models.BooleanField(default=True)
    notifications_commandes = models.BooleanField(default=True)
    notifications_paiements = models.BooleanField(default=True)
    notifications_marketing = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'notifications_preference'
        verbose_name = 'Préférence Notification'
        verbose_name_plural = 'Préférences Notifications'
    
    def __str__(self):
        return f"Préférences - {self.user.nom_complet}"