"""
Settings pour production
"""
from .base import *
import dj_database_url
import os

DEBUG = False

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# Database PostgreSQL en production
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    raise ValueError("DATABASE_URL environment variable is not set!")

# CORS
cors_origins = os.environ.get('CORS_ORIGINS', '')
if cors_origins:
    CORS_ALLOWED_ORIGINS = [
        origin.strip() for origin in cors_origins.split(',') 
        if origin.strip()
    ]
else:
    CORS_ALLOW_ALL_ORIGINS = True  # Temporaire pour test

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Désactiver le logging fichier (Render utilise stdout)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

print("🚀 Mode: PRODUCTION")
print(f"💾 Database: PostgreSQL")
print(f"🔒 Security: Activée")