#!/bin/bash

# Script d'arrêt pour l'application
# Usage: ./stop.sh [clean]

echo "Arrêt de l'API "
echo "========================================="

# Vérifier si l'option 'clean' est passée
if [ "$1" = "clean" ]; then
    echo "Arrêt avec nettoyage du cache..."
    docker-compose down -v
    docker image prune -f
    echo "Application arrêtée et cache aussi "
else
    # Arrêter et supprimer les conteneurs
    docker-compose down
    echo "Application arrêtée"
fi

echo ""
echo "💡 Options disponibles :"
echo "   ./stop.sh        - Arrêt simple"
echo "   ./stop.sh clean  - Arrêt + nettoyage du cache"
echo "   ./clean.sh       - Nettoyage complet"
echo ""