# 🛒 API de Gestion de Commandes

Application web complète pour la gestion de commandes avec API Flask et interface utilisateur.

## 🚀 Démarrage rapide

### Prérequis
- Docker et Docker Compose installés
- Ports 5002 et 6379 disponibles

### Lancement
```bash
./start.sh
```

### Arrêt
```bash
# Arrêt simple
./stop.sh

# Arrêt avec nettoyage du cache
./stop.sh clean
```

### Nettoyage du cache (manuel)
```bash
# Nettoyage complet du cache Docker
./clean.sh
```

> **💡 Note :** Le nettoyage du cache est maintenant manuel pour vous donner le contrôle total. Utilisez `./clean.sh` si vous rencontrez des problèmes ou souhaitez libérer de l'espace disque.

## 🌐 Interface

Une fois démarré, accédez à l'application :
- **Interface web** : http://localhost:5002/test
- **API produits** : http://localhost:5002/api/products
- **API racine** : http://localhost:5002/

## 📋 Fonctionnalités

### Interface utilisateur
- Gestion des produits
- Création de commandes
- Ajout d'adresses de livraison
- Processus de paiement
- Calcul automatique des taxes et frais d'expédition

### API REST
- `GET /api/products` - Liste des produits
- `POST /order` - Création de commande
- `GET /order/{id}` - Consultation de commande
- `PUT /order/{id}` - Modification (adresse/paiement)

## 💰 Règles de calcul

### Frais d'expédition
- ≤ 500g : 5,00 $ CAD
- ≤ 2kg : 10,00 $ CAD  
- > 2kg : 25,00 $ CAD

### Taxes provinciales
- QC : 15% | ON : 13% | AB : 5% | BC : 12% | NS : 14%
- Autres provinces : 0%

## 🔧 Architecture

- **Backend** : Flask + Redis + PostgreSQL
- **Frontend** : HTML/JS/CSS
- **Worker** : RQ (Redis Queue) pour paiements asynchrones
- **Base de données** : PostgreSQL + Redis (cache)
- **Déploiement** : Docker Compose

## 📁 Structure du projet

```
WebAvanc-es/
├── start.sh              # Script de démarrage
├── stop.sh               # Script d'arrêt
├── clean.sh              # Script de nettoyage du cache
├── app.py                # Application Flask principale
├── requirements.txt      # Dépendances Python
├── docker-compose.yml    # Configuration Docker
├── Dockerfile           # Image Docker
├── App/                 # Module application
│   ├── models.py        # Modèles de base de données
│   ├── routes.py        # Routes API
│   ├── services.py      # Logique métier
│   ├── worker.py        # Worker RQ
│   ├── config.py        # Configuration
│   └── redis_client.py  # Client Redis
├── static/              # Ressources statiques
│   ├── css/style.css
│   └── js/app.js
└── templates/           # Templates HTML
    └── index.html       # Interface utilisateur
```

## 🛠️ Commandes utiles

```bash
# Voir les logs
docker-compose logs -f api
docker-compose logs -f worker

# Vérifier l'état des services
docker-compose ps

# Accès direct aux conteneurs
docker-compose exec api bash
docker-compose exec redis redis-cli
```

## 🧪 Test de l'API

### Via l'interface web
Accédez à http://localhost:5002/test pour une interface complète.

### Via curl
```bash
# Lister les produits
curl http://localhost:5002/api/products

# Créer une commande
curl -X POST http://localhost:5002/order \
  -H "Content-Type: application/json" \
  -d '{"products":[{"id":1,"quantity":2}]}'

# Consulter une commande
curl http://localhost:5002/order/1
```

---

*Projet fonctionnel - Version finale optimisée*
