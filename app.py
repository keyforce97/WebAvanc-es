from flask import Flask
from App.models import db, Product, Order
from App.services import fetch_and_store_products
from App.routes import bp as routes_bp  # Import du Blueprint


def create_app():
    app = Flask(__name__)
    
    app.config['DATABASE'] = 'database.db'
    db.init('database.db')

    # Enregistrer les routes
    app.register_blueprint(routes_bp)

    @app.cli.command("init-db")
    def init_db():
        with db:
            db.drop_tables([Product, Order])
            db.create_tables([Product, Order])
            fetch_and_store_products()
            print("Base de données initialisée et produits importés !")

    return app

app = create_app()

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