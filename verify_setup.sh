#!/bin/bash

# Script de vérification des dépendances et de l'installation
echo "🔍 Vérification des dépendances et de l'installation"
echo "=================================================="

echo "📋 Vérification des fichiers..."

# Vérifier que les fichiers essentiels existent
files_to_check=(
    "requirements.txt"
    "docker-compose.yml"
    "Dockerfile"
    "app.py"
    "App/models.py"
    "App/routes.py"
    "App/services.py"
    "App/config.py"
    "App/redis_client.py"
    "templates/index.html"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - MANQUANT"
    fi
done

echo ""
echo "🔍 Vérification des dépendances Python..."

# Afficher le contenu du requirements.txt
echo "📦 Requirements.txt:"
cat requirements.txt

echo ""
echo "🐳 Vérification Docker..."

# Vérifier que Docker est disponible
if command -v docker &> /dev/null; then
    echo "✅ Docker installé"
    if docker info &> /dev/null; then
        echo "✅ Docker démon actif"
    else
        echo "❌ Docker démon inactif"
    fi
else
    echo "❌ Docker non installé"
fi

# Vérifier Docker Compose
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose installé"
else
    echo "❌ Docker Compose non installé"
fi

echo ""
echo "🧪 Test de construction de l'image..."
echo "⚠️  Ceci va construire l'image Docker pour vérifier les dépendances"
read -p "Continuer ? (y/n): " confirm

if [[ $confirm == [yY] ]]; then
    echo "🔨 Construction de l'image de test..."
    if docker build -t test-deps . &> /dev/null; then
        echo "✅ Image construite avec succès"
        echo "✅ Toutes les dépendances sont correctes"
        
        # Nettoyer l'image de test
        docker rmi test-deps &> /dev/null
    else
        echo "❌ Erreur lors de la construction"
        echo "💡 Vérifiez les logs avec : docker build ."
    fi
else
    echo "⏭️  Test de construction ignoré"
fi

echo ""
echo "📊 Résumé :"
echo "- Application : API de gestion de commandes"
echo "- Base de données : PostgreSQL + Redis"
echo "- Framework : Flask + Peewee ORM"
echo "- Worker : RQ (Redis Queue)"
echo "- Interface : HTML/JS/CSS"
echo ""
echo "🚀 Pour démarrer : ./start.sh"
