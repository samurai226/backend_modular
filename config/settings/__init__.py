"""
Settings package
Charge automatiquement les settings selon l'environnement
"""
import os

# Déterminer quel fichier de settings charger
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'development')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'test':
    from .test import *
else:
    from .development import *

print(f"🚀 Chargement des settings: {ENVIRONMENT}")
