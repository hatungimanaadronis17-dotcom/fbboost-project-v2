#!/bin/bash

echo "🔍 Vérification du projet fbboost..."
echo "--------------------------------------"

# 1. Vérifier la présence du dossier migrations
if [ -d "users/migrations" ]; then
    echo "📁 Dossier migrations trouvé : users/migrations/"
else
    echo "❌ ERREUR : Aucun dossier migrations dans users/"
    exit 1
fi

# 2. Lister les fichiers de migrations
echo ""
echo "📄 Fichiers de migration disponibles :"
ls users/migrations

# 3. Vérifier si les migrations sont reconnues par Django
echo ""
echo "🔎 Analyse des migrations appliquées :"
python manage.py showmigrations users

# 4. Vérifier si la table users_profile existe dans la base
echo ""
echo "🗄 Vérification de la table 'users_profile' dans SQLite..."
echo ".tables" | sqlite3 db.sqlite3 | grep users_profile > /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Table 'users_profile' trouvée dans la base SQLite."
else
    echo "❌ Table 'users_profile' ABSENTE dans db.sqlite3 !!!"
    echo "➡ Cela cause l’erreur : no such table: users_profile"
    echo "➡ Il faut exécuter : python manage.py makemigrations && python manage.py migrate"
fi

echo ""
echo "🎉 Vérification terminée."
