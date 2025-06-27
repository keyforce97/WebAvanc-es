# API 8INF349 - Système de Gestion de Commandes

## Installation et Démarrage

### Prérequis
- Docker et Docker Compose
- Ports 5432, 6379 et 5000 disponibles

# cd WebAvanc-es

# 2. Lancer  Docker 
docker-compose up -d

# 3. Initialiser la base de données
docker-compose exec api flask init-db

# 4. Accéder à l'application
# Interface web: http://localhost:5002
# API: http://localhost:5002/api/products
```

## Commandes importantes

```
# Lister les produits
curl http://localhost:5002/api/products

# Créer une commande
curl -X POST http://localhost:5002/order \
  -H "Content-Type: application/json" \
  -d '{"products":[{"id":1,"quantity":2}]}'
### Initialisation manuelle (si nécessaire)
```bash

# Initialiser la base
flask init-db

# Lancer le worker RQ
flask worker
```




### Docker
```bash

# Build de l'image
docker build -t api8inf349 .

# Lancement manuel
docker run -e REDIS_URL=redis://localhost -e DB_HOST=localhost -e DB_USER=user -e DB_PASSWORD=pass -e DB_PORT=5432 -e DB_NAME=api8inf349 api8inf349
```





```bash
# Lister les produits
curl http://localhost:5002/api/products

# Créer une commande
curl -X POST http://localhost:5002/order \
  -H "Content-Type: application/json" \
  -d '{"products":[{"id":1,"quantity":2}]}'
```
