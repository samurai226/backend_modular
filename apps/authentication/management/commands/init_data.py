from django.core.management.base import BaseCommand
from apps.authentication.models import Role
from apps.geography.models import Pays, Ville, Gare


class Command(BaseCommand):
    help = 'Initialise les roles et donnees de base'

    def handle(self, *args, **options):
        self.stdout.write('=== INITIALISATION ===\n')
        
        # Roles
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
                self.stdout.write(f"  Role cree: {role.nom}")
        
        # Burkina Faso
        bf, created = Pays.objects.get_or_create(
            code='BF',
            defaults={'nom': 'Burkina Faso', 'indicatif': '+226'}
        )
        
        # Villes
        villes = [
            {'nom': 'Ouagadougou', 'population': 2500000},
            {'nom': 'Bobo-Dioulasso', 'population': 900000},
        ]
        
        for v in villes:
            Ville.objects.get_or_create(nom=v['nom'], pays=bf, defaults={'population': v['population']})
        
        # Gare
        ouaga = Ville.objects.get(nom='Ouagadougou')
        Gare.objects.get_or_create(
            nom='Gare Routiere de Ouagadougou',
            ville=ouaga,
            defaults={'is_active': True}
        )
        
        self.stdout.write(self.style.SUCCESS('Initialisation terminee!'))