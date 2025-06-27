#!/bin/bash

# Script de nettoyage du projet
# Usage: ./clean.sh

echo "🧹 Nettoyage du projet..."
echo "=========================="


echo "  Suppression du cache Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
find . -name "*.pyd" -delete 2>/dev/null || true

# Supprimer les fichiers système macOS
echo "  Suppression des fichiers système macOS..."
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name ".DS_Store?" -delete 2>/dev/null || true
find . -name "._*" -delete 2>/dev/null || true

# Supprimer les fichiers temporaires
echo "  Suppression des fichiers temporaires..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.bak" -delete 2>/dev/null || true
find . -name "*.swp" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true

# Supprimer les fichiers de test temporaires
echo "  Suppression des fichiers de test..."
rm -f /tmp/test_*.json /tmp/test_*.html 2>/dev/null || true

# Nettoyer les logs Docker (optionnel)
if command -v docker &> /dev/null; then
    echo " Nettoyage Docker (containers arrêtés et images non utilisées)..."
    docker container prune -f 2>/dev/null || true
    docker image prune -f 2>/dev/null || true
fi

echo ""
echo "✅ Nettoyage terminé !"
echo ""
echo "📁 Structure du projet après nettoyage :"
find . -maxdepth 2 -type f | grep -v ".venv" | grep -v ".git" | sort
echo ""
