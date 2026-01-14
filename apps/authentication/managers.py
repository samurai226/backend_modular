"""
Custom managers pour l'app Authentication
"""
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Manager personnalisé pour le modèle User"""
    
    def create_user(self, telephone, password=None, **extra_fields):
        """
        Créer et sauvegarder un utilisateur normal
        """
        if not telephone:
            raise ValueError('Le numéro de téléphone est obligatoire')
        
        user = self.model(telephone=telephone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, telephone, password=None, **extra_fields):
        """
        Créer et sauvegarder un superutilisateur
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(telephone, password, **extra_fields)
