"""
Commande pour initialiser les templates de notifications
"""
from django.core.management.base import BaseCommand
from apps.notifications.models import NotificationTemplate


class Command(BaseCommand):
    help = 'Initialise les templates de notifications'

    def handle(self, *args, **options):
        self.stdout.write('=== INIT NOTIFICATIONS ===\n')
        
        templates = [
            {
                'code': 'RESERVATION_CONFIRMEE',
                'nom': 'Réservation confirmée',
                'type_notification': 'in_app',
                'titre': 'Réservation confirmée',
                'message': 'Bonjour {user}, votre réservation {code} pour {trajet} le {date} est confirmée.',
            },
            {
                'code': 'COLIS_ENREGISTRE',
                'nom': 'Colis enregistré',
                'type_notification': 'in_app',
                'titre': 'Colis enregistré',
                'message': 'Bonjour {user}, votre colis {code} à destination de {destination} a été enregistré.',
            },
            {
                'code': 'COLIS_ARRIVE',
                'nom': 'Colis arrivé',
                'type_notification': 'in_app',
                'titre': 'Colis arrivé',
                'message': 'Le colis {code} est arrivé à destination. Vous pouvez le récupérer.',
            },
            {
                'code': 'COMMANDE_CONFIRMEE',
                'nom': 'Commande confirmée',
                'type_notification': 'in_app',
                'titre': 'Commande confirmée',
                'message': 'Bonjour {user}, votre commande {numero} d\'un montant de {montant} est confirmée.',
            },
            {
                'code': 'PAIEMENT_RECU',
                'nom': 'Paiement reçu',
                'type_notification': 'in_app',
                'titre': 'Paiement reçu',
                'message': 'Bonjour {user}, nous avons reçu votre paiement de {montant}. Nouveau solde: {solde}.',
            },
        ]
        
        for template_data in templates:
            template, created = NotificationTemplate.objects.get_or_create(
                code=template_data['code'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f"Template créé: {template.code}")
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ {NotificationTemplate.objects.count()} templates'))