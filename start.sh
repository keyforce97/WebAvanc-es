#!/bin/bash

# Script de démarrage rapide pour l'application
# Usage: ./start.sh

echo "🚀 Démarrage de l'API de gestion de commandes"
echo "============================================="

# Vérifier que Docker est disponible
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé ou n'est pas dans le PATH"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Le démon Docker n'est pas démarré"
    echo "💡 Veuillez démarrer Docker Desktop ou le démon Docker"
    exit 1
fi

# Arrêter les conteneurs existants s'ils tournent
echo "🛑 Arrêt des conteneurs existants..."
docker-compose down

# Construire et démarrer les services
echo "🔨 Construction et démarrage des services..."
docker-compose up -d --build

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."
sleep 10

# Initialiser la base de données
echo "🗄️ Initialisation de la base de données..."
docker-compose exec api flask init-db

echo ""
echo "✅ Application démarrée avec succès !"
echo ""
echo "🌐 Accès à l'application :"
echo "   - Interface de test : http://localhost:5002/test"
echo "   - API produits      : http://localhost:5002/api/products"
echo "   - API racine        : http://localhost:5002/"
echo ""
echo "🔧 Commandes utiles :"
echo "   - Voir les logs API    : docker-compose logs -f api"
echo "   - Voir les logs Worker : docker-compose logs -f worker"
echo "   - Arrêter             : ./stop.sh"
echo "   - Nettoyer le cache   : ./clean.sh"
echo ""

