"""
Configuration de l'app Authentication
"""
from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentication'
    verbose_name = 'Authentification'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.authentication.signals
        except ImportError:
            pass
