#!/usr/bin/env bash
set -o errexit

echo "Build process..."

# Créer les dossiers nécessaires
mkdir -p logs
mkdir -p media
mkdir -p static
mkdir -p staticfiles

pip install --upgrade pip
pip install -r requirements/production.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Initialiser les donnees
python manage.py init_data

# Creer le superuser
python manage.py create_admin

# Creer les wallets
python manage.py init_payment

echo "Build completed!"