"""
Settings pour l'environnement de développement
"""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Database - SQLite pour développement
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS - Ouvert en développement
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Cache - Simple en développement
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Django Extensions (si installé)
try:
    import django_extensions
    INSTALLED_APPS += ['django_extensions']
except ImportError:
    pass

print("🔧 Mode: DÉVELOPPEMENT")
print(f"📁 Base DIR: {BASE_DIR}")
print(f"💾 Database: SQLite (db.sqlite3)")
