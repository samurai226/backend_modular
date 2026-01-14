from django.core.management.base import BaseCommand
from apps.authentication.models import Role, User


class Command(BaseCommand):
    help = 'Cree un superuser admin'

    def handle(self, *args, **options):
        telephone = '+22670000000'
        
        if User.objects.filter(telephone=telephone).exists():
            self.stdout.write('Admin existe deja')
            return
        
        role_admin = Role.objects.get(nom='admin')
        
        User.objects.create_superuser(
            telephone=telephone,
            password='admin123',
            nom='Admin',
            prenom='Super',
            role=role_admin
        )
        
        self.stdout.write(self.style.SUCCESS('Superuser cree!'))