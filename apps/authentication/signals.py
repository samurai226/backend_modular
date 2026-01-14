"""
Signals pour l'app Authentication
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Signal après la sauvegarde d'un utilisateur
    """
    if created:
        # Actions à effectuer après la création d'un utilisateur
        print(f"✅ Nouvel utilisateur créé: {instance.nom_complet}")
        
        # Ici on pourrait:
        # - Envoyer un email de bienvenue
        # - Créer une notification
        # - Logger l'événement
        # - etc.
