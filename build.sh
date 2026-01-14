#!/usr/bin/env bash
set -o errexit

echo "🔨 Build process..."

pip install --upgrade pip
pip install -r requirements/production.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Initialiser les données
python manage.py init_data

# Créer le superuser
python manage.py create_admin

echo "✅ Build completed!"