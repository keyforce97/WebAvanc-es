#!/bin/bash

# Script pour configurer les permissions des scripts
echo "🔧 Configuration des permissions des scripts..."

# Liste des scripts à rendre exécutables
scripts=(
    "start.sh"
    "stop.sh"
    "dev_start.sh"
    "worker.sh"
    "test_api.sh"
    "health_check.sh"
    "clean.sh"
    "validate.sh"
    "activate.sh"
    "setup_permissions.sh"
)

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        chmod +x "$script"
        echo "✅ $script - permissions configurées"
    else
        echo "⚠️  $script - fichier non trouvé"
    fi
done

echo ""
echo "🎯 Scripts disponibles:"
echo "  ./start.sh          - Démarrer avec Docker"
echo "  ./dev_start.sh      - Démarrer en développement local"
echo "  ./worker.sh         - Démarrer le worker RQ"
echo "  ./test_api.sh       - Tests complets de l'API"
echo "  ./health_check.sh   - Vérifier la santé du système"
echo "  ./clean.sh          - Nettoyer l'environnement"
echo "  ./validate.sh       - Script de validation (legacy)"
echo ""
echo "✅ Configuration terminée !"
