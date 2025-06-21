import os
import redis

# Connexion Redis via l'URL d'environnement
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost')
redis_client = redis.Redis.from_url(REDIS_URL)