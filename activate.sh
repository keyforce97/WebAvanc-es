#!/bin/bash

# Script d'activation de l'environnement de développement
# Usage: source ./activate.sh

# Activer l'environnement virtuel
source .venv/bin/activate

# Définir les variables d'environnement pour le développement local
export FLASK_APP=app.py
export FLASK_ENV=development
export DB_HOST=localhost
export DB_USER=user
export DB_PASSWORD=pass
export DB_PORT=5432
export DB_NAME=api8inf349
export REDIS_URL=redis://localhost:6379

echo "🚀 Environnement de développement activé !"
echo ""
echo "📋 Variables d'environnement définies :"
echo "   FLASK_APP=$FLASK_APP"
echo "   FLASK_ENV=$FLASK_ENV"
echo "   DB_HOST=$DB_HOST"
echo "   REDIS_URL=$REDIS_URL"
echo ""
echo "🔧 Commandes disponibles :"
echo "   flask run          # Lancer l'application (port défini par Flask)"
echo "   flask init-db      # Initialiser la base"
echo "   flask worker       # Lancer le worker RQ"
echo "   python app.py      # Lancer directement (port 5001)"
echo "   python dev_app.py  # Mode développement simplifié (sans DB)"
echo ""
echo "⚠️  Note: Pour le développement local, vous devez avoir:"
echo "   - PostgreSQL en cours d'exécution sur localhost:5432"
echo "   - Redis en cours d'exécution sur localhost:6379"
echo "   - Ou utiliser Docker: docker-compose up -d db redis"
echo ""
echo "🌐 URLs:"
echo "   - Application locale: http://localhost:5001"
echo "   - Docker: http://localhost:5002"
echo ""
