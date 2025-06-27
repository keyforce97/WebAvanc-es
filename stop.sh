#!/bin/bash

# Script d'arrêt pour l'application
# Usage: ./stop.sh

echo "🛑 Arrêt de l'API de gestion de commandes"
echo "========================================="

# Arrêter et supprimer les conteneurs
docker-compose down

echo "✅ Application arrêtée avec succès !"
echo ""
echo "💡 Pour supprimer aussi les volumes (base de données) :"
echo "   docker-compose down -v"
echo ""
