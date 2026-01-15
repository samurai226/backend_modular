from django.core.management.base import BaseCommand
from apps.delivery.models import Colis, HistoriqueEtatColis
from apps.transport.models import Trajet
from apps.geography.models import Gare
from apps.authentication.models import User
from decimal import Decimal


class Command(BaseCommand):
    help = 'Initialise des colis de test'

    def handle(self, *args, **options):
        self.stdout.write('=== INIT DELIVERY ===\n')
        
        # Récupérer des données
        user = User.objects.filter(role__nom='client').first()
        trajet = Trajet.objects.first()
        
        if not user or not trajet:
            self.stdout.write(self.style.ERROR('Données manquantes'))
            return
        
        # Créer un colis
        colis, created = Colis.objects.get_or_create(
            code_suivi='COL-TEST001',
            defaults={
                'expediteur': user,
                'nom_expediteur': 'Jean Dupont',
                'telephone_expediteur': '+22670111111',
                'nom_destinataire': 'Marie Martin',
                'telephone_destinataire': '+22670222222',
                'adresse_destinataire': 'Secteur 15, Ouaga',
                'trajet': trajet,
                'gare_depart': trajet.gare_depart,
                'gare_arrivee': trajet.gare_arrivee,
                'description': 'Documents importants',
                'poids': Decimal('2.5'),
                'type_colis': 'document',
                'prix': Decimal('2000.00'),
                'est_paye': True,
                'statut': 'enregistre'
            }
        )
        
        if created:
            self.stdout.write(f"Colis créé: {colis.code_suivi}")
            
            # Historique
            HistoriqueEtatColis.objects.create(
                colis=colis,
                statut='enregistre',
                commentaire='Colis enregistré à la gare',
                localisation=colis.gare_depart,
                agent=user
            )
        
        self.stdout.write(self.style.SUCCESS('\nDelivery initialisé!'))