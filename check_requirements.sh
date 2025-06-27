#!/bin/bash

# Script de vérification des exigences du projet
# Usage: ./check_requirements.sh

echo "🎯 Vérification des Exigences du Projet"
echo "======================================"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction de vérification
check_requirement() {
    local name="$1"
    local command="$2"
    local expected="$3"
    
    echo -n "Vérification $name... "
    
    if eval "$command" &>/dev/null; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ ÉCHEC${NC}"
        if [ ! -z "$expected" ]; then
            echo "   💡 Attendu: $expected"
        fi
        return 1
    fi
}

# Compteur d'erreurs
errors=0

echo -e "\n${YELLOW}1. Infrastructure Docker${NC}"
check_requirement "Docker Compose" "docker-compose --version" || ((errors++))
check_requirement "Services démarrés" "docker-compose ps | grep -q 'Up'" || ((errors++))

echo -e "\n${YELLOW}2. Services Obligatoires${NC}"
check_requirement "PostgreSQL v12" "docker-compose exec -T db psql -U user -d api8inf349 -c 'SELECT version();' | grep -q 'PostgreSQL 12'" || ((errors++))
check_requirement "Redis actif" "docker-compose exec -T redis redis-cli ping | grep -q 'PONG'" || ((errors++))
check_requirement "API accessible" "curl -s -f http://localhost:5002/api/products > /dev/null" || ((errors++))

echo -e "\n${YELLOW}3. Base de Données${NC}"
check_requirement "Tables créées" "docker-compose exec -T db psql -U user -d api8inf349 -c '\dt' | grep -q 'product'" || ((errors++))
check_requirement "Produits importés" "curl -s http://localhost:5002/api/products | grep -q 'Brown eggs'" || ((errors++))

echo -e "\n${YELLOW}4. Worker RQ (Session 2)${NC}"
# Vérifier si le worker tourne (plus complexe)
if docker-compose exec -T api ps aux | grep -q "rq worker" 2>/dev/null; then
    echo -e "Worker RQ... ${GREEN}✅ OK${NC}"
else
    echo -e "Worker RQ... ${RED}❌ ÉCHEC${NC}"
    echo "   💡 Démarrer avec: docker-compose exec api rq worker default"
    ((errors++))
fi

echo -e "\n${YELLOW}5. Fonctionnalités Core${NC}"
# Test création commande simple
ORDER_TEST=$(curl -s -w "%{http_code}" -o /dev/null -X POST http://localhost:5002/order \
    -H "Content-Type: application/json" \
    -d '{"products": [{"id": 1, "quantity": 1}]}')

if [ "$ORDER_TEST" = "302" ]; then
    echo -e "Création commande... ${GREEN}✅ OK${NC}"
else
    echo -e "Création commande... ${RED}❌ ÉCHEC (code: $ORDER_TEST)${NC}"
    ((errors++))
fi

# Résumé final
echo -e "\n========================================="
if [ $errors -eq 0 ]; then
    echo -e "${GREEN}🎉 TOUTES LES EXIGENCES SONT RESPECTÉES !${NC}"
    echo -e "\n✅ Votre application est prête pour les tests"
    echo "🌐 Interface: http://localhost:5002/test"
    echo "📚 Guide complet: cat GUIDE_TEST.md"
else
    echo -e "${RED}❌ $errors EXIGENCE(S) NON RESPECTÉE(S)${NC}"
    echo -e "\n🔧 Actions recommandées:"
    echo "1. docker-compose down -v"
    echo "2. docker-compose up -d --build"
    echo "3. docker-compose exec api flask init-db"
    echo "4. docker-compose exec api rq worker default (terminal séparé)"
    echo "5. Relancer ce script"
fi

echo -e "\n📋 Pour les détails: ./validate.sh"
echo "🧪 Tests automatiques: ./test_api.sh"

exit $errors
