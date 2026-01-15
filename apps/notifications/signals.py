"""
Signals pour créer automatiquement des notifications
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.transport.models import Reservation
from apps.delivery.models import Colis
from apps.shop.models import Commande
from apps.payment.models import Transaction

from .utils import (
    notifier_reservation_confirmee,
    notifier_colis_enregistre,
    notifier_colis_arrive,
    notifier_commande_confirmee,
    notifier_paiement_recu
)


@receiver(post_save, sender=Reservation)
def notification_reservation(sender, instance, created, **kwargs):
    """Notifier lors de la création/modification d'une réservation"""
    if instance.statut == 'confirmee':
        notifier_reservation_confirmee(instance)


@receiver(post_save, sender=Colis)
def notification_colis(sender, instance, created, **kwargs):
    """Notifier lors de la création/modification d'un colis"""
    if created:
        notifier_colis_enregistre(instance)
    elif instance.statut == 'arrive':
        notifier_colis_arrive(instance)


@receiver(post_save, sender=Commande)
def notification_commande(sender, instance, created, **kwargs):
    """Notifier lors de la confirmation d'une commande"""
    if instance.statut == 'confirmee':
        notifier_commande_confirmee(instance)


@receiver(post_save, sender=Transaction)
def notification_transaction(sender, instance, created, **kwargs):
    """Notifier lors d'une transaction réussie"""
    if created and instance.statut == 'reussie':
        if instance.type_transaction in ['depot', 'transfert_recu']:
            notifier_paiement_recu(instance)