#!/bin/bash

# Script de rollback vers la version stable v1.2
# Usage: ./rollback_v1.2.sh

echo "🔄 ROLLBACK VERS VERSION STABLE v1.2"
echo "===================================="

# Vérifier qu'on est dans un repo Git
if [ ! -d ".git" ]; then
    echo "❌ Erreur: Pas dans un dépôt Git"
    exit 1
fi

# Arrêter les services actuels
echo "🛑 Arrêt des services actuels..."
docker-compose down 2>/dev/null || true

# Sauvegarder la branche actuelle
CURRENT_BRANCH=$(git branch --show-current)
echo "💾 Branche actuelle sauvegardée: $CURRENT_BRANCH"

# Checkout vers la version stable
echo "🔄 Retour à la version stable v1.2..."
git checkout v1.2-stable

if [ $? -eq 0 ]; then
    echo "✅ Rollback réussi vers v1.2-stable"
    
    # Redémarrer l'application
    echo "🚀 Redémarrage de l'application..."
    ./start.sh
    
    echo ""
    echo "🎉 ROLLBACK TERMINÉ !"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ Application restaurée à la version stable v1.2"
    echo "🌐 Interface disponible: http://localhost:5002"
    echo ""
    echo "📋 Pour revenir à la branche précédente:"
    echo "   git checkout $CURRENT_BRANCH"
    echo ""
    echo "📝 Documentation: VERSION_STABLE_v1.2.md"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "❌ Erreur lors du rollback"
    echo "💡 Vérifiez que le tag v1.2-stable existe: git tag -l"
    exit 1
fi
