"""
Commande pour initialiser les wallets
"""
from django.core.management.base import BaseCommand
from apps.payment.models import Wallet
from apps.authentication.models import User
from decimal import Decimal


class Command(BaseCommand):
    help = 'Initialise les wallets pour les users'

    def handle(self, *args, **options):
        self.stdout.write('=== INIT PAYMENT ===\n')
        
        # Créer un wallet pour chaque user
        users = User.objects.all()
        
        for user in users:
            wallet, created = Wallet.objects.get_or_create(
                user=user,
                defaults={'solde': Decimal('10000.00')}
            )
            
            if created:
                self.stdout.write(f"Wallet cree: {user.nom_complet} - 10,000 FCFA")
            else:
                self.stdout.write(f"Wallet existe: {user.nom_complet} - {wallet.solde} FCFA")
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ {Wallet.objects.count()} wallets'))