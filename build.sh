#!/usr/bin/env bash
set -o errexit

echo "Build process..."

pip install --upgrade pip
pip install -r requirements/production.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Initialiser les donnees
python manage.py init_data

# Creer le superuser
python manage.py create_admin

echo "Build completed!"