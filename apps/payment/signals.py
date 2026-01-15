"""
Signals Payment
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.authentication.models import User
from .models import Wallet


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    """Créer automatiquement un wallet pour chaque nouveau user"""
    if created:
        Wallet.objects.create(user=instance)