#!/bin/bash

# Script de validation de l'API
# Usage: ./validate.sh
# Prérequis: L'application doit être démarrée (./start.sh)

API_BASE="http://localhost:5002"

echo "🧪 Validation de l'API de gestion de commandes"
echo "==============================================="

# Test 1: Récupération des produits
echo "📦 Test 1: Récupération des produits..."
response=$(curl -s -w "%{http_code}" -o /tmp/products.json "$API_BASE/api/products")
if [ "$response" = "200" ]; then
    echo "✅ OK - Produits récupérés"
    product_count=$(cat /tmp/products.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('products', [])))")
    echo "   Nombre de produits: $product_count"
else
    echo "❌ ERREUR - Code HTTP: $response"
fi

# Test 2: Création d'une commande
echo "🛒 Test 2: Création d'une commande..."
order_response=$(curl -s -X POST "$API_BASE/order" \
    -H "Content-Type: application/json" \
    -d '{"products": [{"id": 1, "quantity": 2}]}' \
    -w "%{http_code}" -o /tmp/order_create.txt)

if [ "$order_response" = "302" ]; then
    echo "✅ OK - Commande créée (redirection)"
    # Extraire l'ID de la commande depuis la redirection
    order_id=$(curl -s -X POST "$API_BASE/order" \
        -H "Content-Type: application/json" \
        -d '{"products": [{"id": 1, "quantity": 2}]}' \
        -w "%{redirect_url}" -o /dev/null | sed 's/.*order\///')
    echo "   ID de commande: $order_id"
else
    echo "❌ ERREUR - Code HTTP: $order_response"
    cat /tmp/order_create.txt
fi

# Test 3: Récupération de la commande
if [ ! -z "$order_id" ]; then
    echo "📋 Test 3: Récupération de la commande $order_id..."
    get_response=$(curl -s -w "%{http_code}" -o /tmp/order_get.json "$API_BASE/order/$order_id")
    if [ "$get_response" = "200" ]; then
        echo "✅ OK - Commande récupérée"
        total_price=$(cat /tmp/order_get.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('order', {}).get('total_price', 'N/A'))")
        echo "   Prix total: $total_price"
    else
        echo "❌ ERREUR - Code HTTP: $get_response"
    fi
    
    # Test 4: Tentative de paiement
    echo "💳 Test 4: Tentative de paiement asynchrone..."
    pay_response=$(curl -s -X PUT "$API_BASE/order/$order_id" \
        -H "Content-Type: application/json" \
        -d '{
            "email": "test@example.com",
            "credit_card": {
                "name": "John Doe",
                "number": "4242424242424242",
                "expiration_month": 12,
                "expiration_year": 2025,
                "cvv": "123"
            }
        }' \
        -w "%{http_code}" -o /tmp/payment.txt)
    
    if [ "$pay_response" = "202" ]; then
        echo "✅ OK - Paiement en cours (202 Accepted)"
        echo "   Attente du traitement par le worker..."
        sleep 5
        
        # Vérifier le statut après traitement
        final_response=$(curl -s -w "%{http_code}" -o /tmp/order_final.json "$API_BASE/order/$order_id")
        if [ "$final_response" = "200" ]; then
            paid_status=$(cat /tmp/order_final.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('order', {}).get('paid', False))")
            echo "   Statut final payé: $paid_status"
        fi
    else
        echo "❌ ERREUR - Code HTTP: $pay_response"
        cat /tmp/payment.txt
    fi
fi

# Test 5: Interface web
echo "🌐 Test 5: Interface de test..."
web_response=$(curl -s -w "%{http_code}" -o /tmp/web.html "$API_BASE/test")
if [ "$web_response" = "200" ]; then
    echo "✅ OK - Interface accessible"
else
    echo "❌ ERREUR - Code HTTP: $web_response"
fi

echo ""
echo "📊 Résumé des tests"
echo "==================="
echo "URL de l'application: $API_BASE"
echo "Interface de test: $API_BASE/test"
echo ""
echo "🗂️ Fichiers de sortie:"
echo "   - /tmp/products.json    - Liste des produits"
echo "   - /tmp/order_get.json   - Détails de commande"
echo "   - /tmp/order_final.json - État final après paiement"
echo "   - /tmp/web.html         - Page de test"
echo ""

# Nettoyage optionnel
# rm -f /tmp/products.json /tmp/order_*.json /tmp/payment.txt /tmp/web.html
