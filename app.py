from flask import Flask
from App.models import db, Product, Order, OrderProduct
from App.services import fetch_and_store_products
from App.routes import bp as routes_bp
import click
from flask.cli import with_appcontext

# Création de l'app Flask
app = Flask(__name__)

# Enregistrement du Blueprint
app.register_blueprint(routes_bp)

# Commande CLI pour initialiser la base
@app.cli.command("init-db")
@with_appcontext
def init_db():
    """Initialise la base de données (tables)."""
    with db:
        db.create_tables([Product, Order, OrderProduct])
    fetch_and_store_products()
    print("Base de données initialisée et produits importés !")

    return app

#Test de paiement
"""
from flask import request, jsonify

@app.route('/simulate_payment', methods=['POST'])
def simulate_payment():
    data = request.get_json()
    return jsonify({
        "success": True,
        "transaction": {
            "id": "txn_123456789",
            "status": "approved"
        }
    }), 200
"""