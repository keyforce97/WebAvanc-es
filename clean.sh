#!/bin/bash

# Script de nettoyage complet du cache de l'application
# Usage: ./clean.sh

echo "🧹 Nettoyage complet du cache de l'application"
echo "============================================="

# Arrêter tous les conteneurs
echo "🛑 Arrêt de tous les conteneurs..."
docker-compose down -v

# Nettoyage Docker complet
echo "🗑️ Nettoyage Docker complet..."
echo "   - Suppression des conteneurs arrêtés..."
docker container prune -f

echo "   - Suppression des images orphelines..."
docker image prune -f

echo "   - Suppression des réseaux inutilisés..."
docker network prune -f

echo "   - Suppression des volumes orphelins..."
docker volume prune -f

echo "   - Nettoyage du cache de build..."
docker builder prune -f

# Nettoyage des logs
echo "📝 Nettoyage des logs Docker..."
docker system events --since 1s --until 1s > /dev/null 2>&1

# Nettoyage optionnel total (décommenté si nécessaire)
# echo "⚠️ Nettoyage total du système Docker (ATTENTION: supprime TOUTES les images)..."
# docker system prune -a -f

echo ""
echo "✅ Nettoyage terminé !"
echo ""
echo "📊 Espace récupéré :"
docker system df

echo ""
echo "💡 Pour redémarrer l'application après nettoyage :"
echo "   ./start.sh"
echo ""
