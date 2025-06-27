#!/usr/bin/env python3
"""
Version de développement simple de l'application qui peut tourner sans PostgreSQL/Redis.
Usage: python dev_app.py
"""

from flask import Flask, jsonify, render_template_string

# Application Flask simple pour les tests
dev_app = Flask(__name__)

# Template HTML simple pour les tests
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>API Commandes - Mode Développement</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background-color: #d4edda; color: #155724; }
        .warning { background-color: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <h1>🚀 API de Gestion de Commandes</h1>
    <div class="status warning">
        <strong>Mode Développement</strong><br>
        Cette version simplifiée fonctionne sans PostgreSQL/Redis.
    </div>
    
    <h2>📋 Endpoints disponibles</h2>
    <ul>
        <li><a href="/api/products">/api/products</a> - Liste des produits (simulée)</li>
        <li><a href="/status">/status</a> - Statut de l'application</li>
        <li><a href="/">/</a> - Cette page</li>
    </ul>
    
    <h2>🔧 Pour la version complète</h2>
    <ol>
        <li>Lancer les services: <code>docker-compose up -d</code></li>
        <li>Initialiser la DB: <code>docker-compose exec api flask init-db</code></li>
        <li>Accéder à: <a href="http://localhost:5002">http://localhost:5002</a></li>
    </ol>
</body>
</html>
"""

@dev_app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@dev_app.route('/api/products')
def products():
    # Simulation de données produits
    return jsonify({
        "products": [
            {"id": 1, "name": "Produit Test 1", "price": 19.99, "in_stock": True},
            {"id": 2, "name": "Produit Test 2", "price": 29.99, "in_stock": True},
            {"id": 3, "name": "Produit Test 3", "price": 39.99, "in_stock": False}
        ]
    })

@dev_app.route('/status')
def status():
    return jsonify({
        "status": "OK",
        "mode": "development",
        "message": "Application en mode développement simplifié",
        "database": "simulée",
        "redis": "simulé"
    })

if __name__ == '__main__':
    print("🚀 Lancement de l'application en mode développement...")
    print("📍 URL: http://localhost:5001")
    print("⚠️  Mode simplifié sans base de données")
    print("🛑 Arrêt: Ctrl+C")
    print("")
    
    dev_app.run(debug=True, host='0.0.0.0', port=5001)
