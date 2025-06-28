# API 8INF349 - Système de Gestion de Commandes



# 1. Démarrage de l'application 
```bash
# Arrêter les conteneurs existants si ça a été démarré avant
docker-compose down

# Démarrer les services
docker-compose up -d

# Initialiser la base de données
docker-compose exec api flask init-db
```

# 2. Accès à l'applicationConfig
- ConfigInterface webConfig : http://localhost:5002
- ConfigAPI produitsConfig : http://localhost:5002/api/products

# Config3. Tests API via curlConfig
```bash
# Lister les produits
curl http://localhost:5002/api/products

# Créer une commande
curl -X POST http://localhost:5002/order \
  -H "Content-Type: application/json" \
  -d '{"products":[{"id":1,"quantity":2}]}'

# Voir une commande (remplacer 1 par l'ID obtenu)
curl http://localhost:5002/order/1


# Config4. Commandes utilesConfig
```bash
# Voir les logs de l'API
docker-compose logs -f api

# Voir les logs du worker
docker-compose logs -f worker

# Voir tous les logs
docker-compose logs -f

# Redémarrer un service
docker-compose restart api

# Arrêter l'application
docker-compose down

# Nettoyer complètement (conteneurs + volumes + images)
docker-compose down -v --rmi all
```

# Structure du projet

```
📁 WebAvanc-es/
├── 📄 app.py                    # Fichier principal (Flask app)
├── 📄 docker-compose.yml       # Configuration Docker (PostgreSQL + Redis + API + Worker)
├── 📄 Dockerfile              # Image Docker pour l'application
├── 📄 requirements.txt        # Dépendances Python
├── 📄 README.md               # Documentation
├── 📄 .gitignore              # Fichiers ignorés par Git
│
├── 📁 App/                    # Module principal de l'application
│   ├── 📄 __init__.py         # Initialisation du module Flask
│   ├── 📄 config.py           # Configuration (DB, Redis, etc.)
│   ├── 📄 models.py           # Modèles de données (Peewee ORM)
│   ├── 📄 routes.py           # Routes API (/order, /products, etc.)
│   ├── 📄 services.py         # Logique métier (paiement, calculs)
│   ├── 📄 redis_client.py     # Configuration Redis
│   └── 📄 worker.py           # Worker RQ pour paiements asynchrones
│
└── 📁 templates/              # Interface utilisateur
    └── 📄 index.html          # Interface web de test
```




