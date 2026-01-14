"""
Script d'initialisation des données de base
Execute avec: python manage.py shell < scripts/init_data.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import Role


def init_roles():
    """Créer les rôles de base"""
    print("📋 Création des rôles...")
    
    roles_data = [
        {
            'nom': Role.ADMIN,
            'description': 'Administrateur système avec tous les droits'
        },
        {
            'nom': Role.GERANT,
            'description': 'Gérant de gare'
        },
        {
            'nom': Role.GUICHETIER,
            'description': 'Guichetier - Gestion des réservations'
        },
        {
            'nom': Role.COLISSIER,
            'description': 'Colissier - Gestion des colis'
        },
        {
            'nom': Role.LIVREUR,
            'description': 'Livreur - Livraisons à domicile'
        },
        {
            'nom': Role.CLIENT,
            'description': 'Client - Réservations et colis'
        },
        {
            'nom': Role.EXPEDITEUR,
            'description': 'Expéditeur de colis'
        },
        {
            'nom': Role.RECEPTEUR,
            'description': 'Récepteur de colis'
        },
    ]
    
    for role_data in roles_data:
        role, created = Role.objects.get_or_create(
            nom=role_data['nom'],
            defaults={'description': role_data['description']}
        )
        if created:
            print(f"  ✅ Rôle créé: {role.get_nom_display()}")
        else:
            print(f"  ℹ️  Rôle existe déjà: {role.get_nom_display()}")


def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("🚀 INITIALISATION DES DONNÉES - APP AUTHENTICATION")
    print("="*60 + "\n")
    
    try:
        init_roles()
        
        print("\n" + "="*60)
        print("✅ INITIALISATION TERMINÉE")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
