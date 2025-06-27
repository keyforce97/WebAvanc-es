#!/usr/bin/env python3
"""
Worker RQ pour traiter les tâches de paiement en arrière-plan.
Ce script peut être lancé via `flask worker` ou directement avec `python -m App.worker`
"""

import os
import sys
from App.redis_client import redis_client
from rq import Worker

def run_worker():
    """Lance le worker RQ."""
    try:
        # Créer et démarrer le worker directement avec la connexion Redis
        worker = Worker(['default'], connection=redis_client)
        print("Worker RQ démarré. En attente de tâches...")
        worker.work()
    except KeyboardInterrupt:
        print("\nWorker arrêté par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"Erreur du worker: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_worker()

