#!/bin/bash

# Script de test automatique pour l'API de gestion de commandes
# Usage: ./test_api.sh

BASE_URL="http://localhost:5002"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🧪 Tests automatiques de l'API de Gestion de Commandes"
echo "=============================================="

# Test 1: Vérifier que l'API est accessible
echo -e "\n${YELLOW}Test 1: Accessibilité de l'API${NC}"
if curl -s -f "$BASE_URL/api/products" > /dev/null; then
    echo -e "${GREEN}✅ API accessible${NC}"
else
    echo -e "${RED}❌ API inaccessible${NC}"
    echo "💡 Assurez-vous que l'application est démarrée avec ./start.sh"
    exit 1
fi

# Test 2: Lister les produits
echo -e "\n${YELLOW}Test 2: Liste des produits${NC}"
PRODUCTS=$(curl -s "$BASE_URL/api/products")
if echo "$PRODUCTS" | grep -q '"products"'; then
    PRODUCT_COUNT=$(echo "$PRODUCTS" | grep -o '"id"' | wc -l)
    echo -e "${GREEN}✅ $PRODUCT_COUNT produits récupérés${NC}"
else
    echo -e "${RED}❌ Impossible de récupérer les produits${NC}"
fi

# Test 3: Créer une commande Session 1
echo -e "\n${YELLOW}Test 3: Création commande Session 1${NC}"
ORDER_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/order_response.json \
    -X POST "$BASE_URL/order" \
    -H "Content-Type: application/json" \
    -d '{"product": {"id": 1, "quantity": 2}}')

HTTP_CODE="${ORDER_RESPONSE: -3}"
if [ "$HTTP_CODE" = "302" ]; then
    echo -e "${GREEN}✅ Commande créée avec redirection 302${NC}"
    # Extraire l'ID de la commande de la Location header si possible
    ORDER_ID=1  # Supposer que c'est la première commande
else
    echo -e "${RED}❌ Échec création commande (code: $HTTP_CODE)${NC}"
fi

# Test 4: Consulter la commande
echo -e "\n${YELLOW}Test 4: Consultation de commande${NC}"
ORDER_DETAILS=$(curl -s "$BASE_URL/order/$ORDER_ID")
if echo "$ORDER_DETAILS" | grep -q '"order"'; then
    echo -e "${GREEN}✅ Commande consultée avec succès${NC}"
    # Afficher quelques détails
    TOTAL_PRICE=$(echo "$ORDER_DETAILS" | grep -o '"total_price":[^,]*' | cut -d':' -f2 | tr -d ' ')
    SHIPPING_PRICE=$(echo "$ORDER_DETAILS" | grep -o '"shipping_price":[^,]*' | cut -d':' -f2 | tr -d ' ')
    echo "   💰 Prix total: $TOTAL_PRICE CAD"
    echo "   🚚 Frais livraison: $((SHIPPING_PRICE/100)) CAD"
else
    echo -e "${RED}❌ Impossible de consulter la commande${NC}"
fi

# Test 5: Mettre à jour avec adresse (Session 1)
echo -e "\n${YELLOW}Test 5: Mise à jour adresse + taxes${NC}"
UPDATE_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/update_response.json \
    -X PUT "$BASE_URL/order/$ORDER_ID" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "test@example.com",
        "shipping_information": {
            "province": "QC",
            "address": "123 Rue Test",
            "city": "Saguenay",
            "postal_code": "G7H 5K1",
            "country": "Canada"
        }
    }')

HTTP_CODE="${UPDATE_RESPONSE: -3}"
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Adresse mise à jour avec calcul des taxes${NC}"
    
    # Vérifier le recalcul des taxes
    UPDATED_ORDER=$(curl -s "$BASE_URL/order/$ORDER_ID")
    if echo "$UPDATED_ORDER" | grep -q '"total_price_tax"'; then
        TOTAL_WITH_TAX=$(echo "$UPDATED_ORDER" | grep -o '"total_price_tax":[^,]*' | cut -d':' -f2 | tr -d ' ')
        echo "   🧮 Prix avec taxes QC (15%): $TOTAL_WITH_TAX CAD"
    fi
else
    echo -e "${RED}❌ Échec mise à jour adresse (code: $HTTP_CODE)${NC}"
fi

# Test 6: Paiement asynchrone
echo -e "\n${YELLOW}Test 6: Traitement de paiement${NC}"
PAYMENT_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/payment_response.json \
    -X PUT "$BASE_URL/order/$ORDER_ID" \
    -H "Content-Type: application/json" \
    -d '{
        "credit_card": {
            "name": "John Doe",
            "number": "4242424242424242",
            "expiration_month": 12,
            "expiration_year": 2025,
            "cvv": "123"
        }
    }')

HTTP_CODE="${PAYMENT_RESPONSE: -3}"
if [ "$HTTP_CODE" = "202" ]; then
    echo -e "${GREEN}✅ Paiement en cours (202 Accepted)${NC}"
    
    # Attendre le traitement
    echo "   ⏳ Attente du traitement asynchrone (10 secondes)..."
    sleep 10
    
    # Vérifier le statut final
    FINAL_ORDER=$(curl -s "$BASE_URL/order/$ORDER_ID")
    if echo "$FINAL_ORDER" | grep -q '"paid":true'; then
        echo -e "${GREEN}✅ Paiement traité avec succès${NC}"
    else
        echo -e "${YELLOW}⚠️ Paiement en cours ou échec${NC}"
    fi
elif [ "$HTTP_CODE" = "409" ]; then
    echo -e "${YELLOW}⚠️ Commande déjà payée (409 Conflict)${NC}"
else
    echo -e "${RED}❌ Échec paiement (code: $HTTP_CODE)${NC}"
fi

# Test 7: Créer commande multi-produits (Session 2)
echo -e "\n${YELLOW}Test 7: Commande multi-produits Session 2${NC}"
MULTI_ORDER_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/multi_order_response.json \
    -X POST "$BASE_URL/order" \
    -H "Content-Type: application/json" \
    -d '{"products": [{"id": 2, "quantity": 1}, {"id": 3, "quantity": 2}]}')

HTTP_CODE="${MULTI_ORDER_RESPONSE: -3}"
if [ "$HTTP_CODE" = "302" ]; then
    echo -e "${GREEN}✅ Commande multi-produits créée${NC}"
    ORDER_ID_2=2  # Supposer que c'est la deuxième commande
    
    # Consulter pour vérifier
    MULTI_ORDER_DETAILS=$(curl -s "$BASE_URL/order/$ORDER_ID_2")
    if echo "$MULTI_ORDER_DETAILS" | grep -q '"order"'; then
        PRODUCT_COUNT=$(echo "$MULTI_ORDER_DETAILS" | grep -o '"id":[0-9]*' | wc -l)
        echo "   🛍️ $PRODUCT_COUNT produits dans la commande"
    fi
else
    echo -e "${RED}❌ Échec création commande multi-produits${NC}"
fi

# Test 8: Test d'erreur (produit inexistant)
echo -e "\n${YELLOW}Test 8: Gestion d'erreurs${NC}"
ERROR_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/error_response.json \
    -X POST "$BASE_URL/order" \
    -H "Content-Type: application/json" \
    -d '{"product": {"id": 999, "quantity": 1}}')

HTTP_CODE="${ERROR_RESPONSE: -3}"
if [ "$HTTP_CODE" = "422" ]; then
    echo -e "${GREEN}✅ Erreur 422 pour produit inexistant${NC}"
else
    echo -e "${YELLOW}⚠️ Code erreur inattendu: $HTTP_CODE${NC}"
fi

# Résumé final
echo -e "\n${YELLOW}===========================================${NC}"
echo -e "🎯 ${GREEN}Tests terminés${NC}"
echo -e "\n💡 ${YELLOW}Pour tester manuellement:${NC}"
echo "   🌐 Interface web: $BASE_URL/test"
echo "   📚 Documentation: cat QUICK_START.md"
echo "   🔧 Logs: docker-compose logs -f api"

# Nettoyer les fichiers temporaires
rm -f /tmp/order_response.json /tmp/update_response.json /tmp/payment_response.json /tmp/multi_order_response.json /tmp/error_response.json

echo -e "\n✨ Tests automatiques complétés!"
