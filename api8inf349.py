from flask import Flask
from App.models import db, Product, Order, OrderProduct
from App.services import fetch_and_store_products
from App.routes import bp as routes_bp
from App.config import Config
import click
from flask.cli import with_appcontext

def create_app():
    # Création de l'app Flask
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enregistrement du Blueprint
    app.register_blueprint(routes_bp)
    
    #  initialisation de la base
    @app.cli.command("init-db")
    @with_appcontext
    def init_db():
        """Initialise la base de données (tables)."""
        with db:
            db.create_tables([Product, Order, OrderProduct])
        fetch_and_store_products()
        print("Base de données initialisée et produits importés !")
    
    # le worker RQ
    @app.cli.command("worker")
    @with_appcontext
    def worker():
        """Lance le worker RQ pour traiter les tâches en arrière-plan."""
        from App.redis_client import redis_client
        from rq import Worker
        import sys
        
        try:
            worker = Worker(['default'], connection=redis_client)
            print("Worker RQ démarré. En attente de tâches...")
            worker.work()
        except KeyboardInterrupt:
            print("Worker arrêté.")
            sys.exit(0)
    
    return app

# Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
