"""
Commande pour initialiser les données
Usage: python manage.py init_data
"""
from django.core.management.base import BaseCommand
from apps.authentication.models import Role, User
from apps.geography.models import Pays, Ville, Gare


class Command(BaseCommand):
    help = 'Initialise les roles et donnees de base'

    def handle(self, *args, **options):
        self.stdout.write('=== INITIALISATION DES DONNEES ===\n')
        
        # Créer les rôles
        self.stdout.write('Creation des roles...')
        roles_data = [
            {'nom': 'admin', 'description': 'Administrateur systeme'},
            {'nom': 'client', 'description': 'Client'},
            {'nom': 'guichetier', 'description': 'Guichetier'},
            {'nom': 'livreur', 'description': 'Livreur'},
        ]
        
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                nom=role_data['nom'],
                defaults={'description': role_data['description']}
            )
            if created:
                self.stdout.write(f"  ✓ Role cree: {role.nom}")
            else:
                self.stdout.write(f"  - Role existe: {role.nom}")
        
        # Créer le Burkina Faso
        self.stdout.write('\nCreation des donnees geographiques...')
        bf, created = Pays.objects.get_or_create(
            code='BF',
            defaults={'nom': 'Burkina Faso', 'indicatif': '+226'}
        )
        if created:
            self.stdout.write(f"  ✓ Pays cree: {bf.nom}")
        else:
            self.stdout.write(f"  - Pays existe: {bf.nom}")
        
        # Créer les villes
        villes_data = [
            {'nom': 'Ouagadougou', 'population': 2500000},
            {'nom': 'Bobo-Dioulasso', 'population': 900000},
        ]
        
        for ville_data in villes_data:
            ville, created = Ville.objects.get_or_create(
                nom=ville_data['nom'],
                pays=bf,
                defaults={'population': ville_data['population']}
            )
            if created:
                self.stdout.write(f"  ✓ Ville creee: {ville.nom}")
        
        # Créer une gare
        ouaga = Ville.objects.get(nom='Ouagadougou')
        gare, created = Gare.objects.get_or_create(
            nom='Gare Routiere de Ouagadougou',
            ville=ouaga,
            defaults={'is_active': True}
        )
        if created:
            self.stdout.write(f"  ✓ Gare creee: {gare.nom}")
        
        # Résumé
        self.stdout.write(self.style.SUCCESS('\n=== RESUME ==='))
        self.stdout.write(f"Roles: {Role.objects.count()}")
        self.stdout.write(f"Pays: {Pays.objects.count()}")
        self.stdout.write(f"Villes: {Ville.objects.count()}")
        self.stdout.write(f"Gares: {Gare.objects.count()}")
        self.stdout.write(self.style.SUCCESS('\n✓ Initialisation terminee!'))