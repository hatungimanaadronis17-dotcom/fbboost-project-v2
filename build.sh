#!/bin/bash
set -e  # Arrête si erreur

echo "Installation des dépendances..."
pip install -r requirements.txt

echo "Collect static (si besoin)..."
python manage.py collectstatic --noinput || true

echo "Application des migrations..."
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput || true

echo "Création du superuser si absent..."
python manage.py createsuperuser --noinput --verbosity 0 || true

echo "Build terminé !"
