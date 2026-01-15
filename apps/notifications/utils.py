"""
Utilitaires pour l'envoi de notifications
"""
from django.utils import timezone
from .models import Notification, NotificationTemplate, NotificationPreference


def creer_notification(user, template_code, context, type_notification='in_app', **kwargs):
    """
    Créer et envoyer une notification
    
    Args:
        user: L'utilisateur destinataire
        template_code: Code du template à utiliser
        context: Dictionnaire avec les variables du template
        type_notification: Type de notification (in_app, email, sms, push)
        **kwargs: Arguments additionnels (reservation, colis, commande, etc.)
    
    Returns:
        Notification créée
    """
    # Vérifier les préférences de l'utilisateur
    preferences, _ = NotificationPreference.objects.get_or_create(user=user)
    
    # Vérifier si ce type de notification est activé
    type_mapping = {
        'email': preferences.activer_email,
        'sms': preferences.activer_sms,
        'push': preferences.activer_push,
        'in_app': preferences.activer_in_app,
    }
    
    if not type_mapping.get(type_notification, True):
        return None
    
    # Récupérer le template
    try:
        template = NotificationTemplate.objects.get(
            code=template_code,
            type_notification=type_notification,
            is_active=True
        )
    except NotificationTemplate.DoesNotExist:
        # Créer une notification simple sans template
        notification = Notification.objects.create(
            user=user,
            type_notification=type_notification,
            titre=context.get('titre', 'Notification'),
            message=context.get('message', ''),
            **kwargs
        )
        return notification
    
    # Rendre le template
    titre, message = template.render(context)
    
    # Créer la notification
    notification = Notification.objects.create(
        user=user,
        template=template,
        type_notification=type_notification,
        titre=titre,
        message=message,
        data=context,
        **kwargs
    )
    
    # Envoyer la notification selon le type
    if type_notification == 'in_app':
        # Les notifications in-app sont juste créées en DB
        notification.is_sent = True
        notification.sent_at = timezone.now()
        notification.save()
    elif type_notification == 'email':
        envoyer_email(notification)
    elif type_notification == 'sms':
        envoyer_sms(notification)
    elif type_notification == 'push':
        envoyer_push(notification)
    
    return notification


def envoyer_email(notification):
    """Envoyer une notification par email"""
    from django.core.mail import send_mail
    from django.conf import settings
    
    try:
        send_mail(
            subject=notification.titre,
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.user.email] if notification.user.email else [],
            fail_silently=False,
        )
        
        notification.is_sent = True
        notification.sent_at = timezone.now()
        notification.save()
    except Exception as e:
        notification.error_message = str(e)
        notification.save()


def envoyer_sms(notification):
    """Envoyer une notification par SMS"""
    # TODO: Intégrer un service SMS (Twilio, etc.)
    # Pour l'instant, on marque juste comme envoyé
    notification.is_sent = True
    notification.sent_at = timezone.now()
    notification.save()


def envoyer_push(notification):
    """Envoyer une notification push"""
    # TODO: Intégrer Firebase Cloud Messaging
    # Pour l'instant, on marque juste comme envoyé
    notification.is_sent = True
    notification.sent_at = timezone.now()
    notification.save()


# Fonctions helper pour créer des notifications spécifiques

def notifier_reservation_confirmee(reservation):
    """Notifier qu'une réservation est confirmée"""
    context = {
        'user': reservation.client.nom_complet,
        'code': reservation.code_reservation,
        'trajet': f"{reservation.trajet.gare_depart.ville.nom} → {reservation.trajet.gare_arrivee.ville.nom}",
        'date': reservation.trajet.date_depart,
    }
    
    creer_notification(
        user=reservation.client,
        template_code='RESERVATION_CONFIRMEE',
        context=context,
        type_notification='in_app',
        reservation=reservation
    )


def notifier_colis_enregistre(colis):
    """Notifier qu'un colis est enregistré"""
    context = {
        'user': colis.expediteur.nom_complet,
        'code': colis.code_suivi,
        'destination': colis.gare_arrivee.ville.nom,
    }
    
    creer_notification(
        user=colis.expediteur,
        template_code='COLIS_ENREGISTRE',
        context=context,
        type_notification='in_app',
        colis=colis
    )


def notifier_colis_arrive(colis):
    """Notifier qu'un colis est arrivé"""
    context = {
        'user': colis.nom_destinataire,
        'code': colis.code_suivi,
    }
    
    # Notifier l'expéditeur
    creer_notification(
        user=colis.expediteur,
        template_code='COLIS_ARRIVE',
        context=context,
        type_notification='in_app',
        colis=colis
    )
    
    # Notifier le destinataire si enregistré
    if colis.destinataire:
        creer_notification(
            user=colis.destinataire,
            template_code='COLIS_ARRIVE',
            context=context,
            type_notification='in_app',
            colis=colis
        )


def notifier_commande_confirmee(commande):
    """Notifier qu'une commande est confirmée"""
    context = {
        'user': commande.user.nom_complet,
        'numero': commande.numero_commande,
        'montant': f"{commande.total} FCFA",
    }
    
    creer_notification(
        user=commande.user,
        template_code='COMMANDE_CONFIRMEE',
        context=context,
        type_notification='in_app',
        commande=commande
    )


def notifier_paiement_recu(transaction):
    """Notifier qu'un paiement est reçu"""
    context = {
        'user': transaction.user.nom_complet,
        'montant': f"{transaction.montant} FCFA",
        'solde': f"{transaction.solde_apres} FCFA",
    }
    
    creer_notification(
        user=transaction.user,
        template_code='PAIEMENT_RECU',
        context=context,
        type_notification='in_app'
    )