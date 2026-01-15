from django.core.management.base import BaseCommand
from apps.transport.models import Compagnie, Bus, Trajet
from apps.geography.models import Gare
from datetime import date, time
from decimal import Decimal


class Command(BaseCommand):
    help = 'Initialise les donnees transport'

    def handle(self, *args, **options):
        self.stdout.write('=== INIT TRANSPORT ===\n')
        
        # Compagnie
        compagnie, _ = Compagnie.objects.get_or_create(
            nom='STAF Transport',
            defaults={
                'telephone': '+22625123456',
                'email': 'contact@staf.bf',
                'is_active': True
            }
        )
        self.stdout.write(f"Compagnie: {compagnie.nom}")
        
        # Bus
        bus, _ = Bus.objects.get_or_create(
            numero='BF-1234-AB',
            defaults={
                'compagnie': compagnie,
                'modele': 'Mercedes Sprinter',
                'nombre_places': 30,
                'is_active': True
            }
        )
        self.stdout.write(f"Bus: {bus.numero}")
        
        # Trajets
        gares = Gare.objects.filter(is_active=True)[:2]
        if len(gares) >= 2:
            trajet, _ = Trajet.objects.get_or_create(
                gare_depart=gares[0],
                gare_arrivee=gares[1],
                date_depart=date(2026, 1, 20),
                defaults={
                    'compagnie': compagnie,
                    'bus': bus,
                    'heure_depart': time(8, 0),
                    'heure_arrivee_estimee': time(12, 0),
                    'prix': Decimal('5000.00'),
                    'places_disponibles': 30,
                    'statut': 'prevu'
                }
            )
            self.stdout.write(f"Trajet: {trajet}")
        
        self.stdout.write(self.style.SUCCESS('\nTransport initialise!'))