# 🎯 API de Gestion de Commandes - Guide de démarrage rapide

## ✅ Conformité aux exigences

### 1. **Gestion du code et dépôt** ✅
- [x] Fichier `CODES-PERMANENTS` présent à la racine
- [x] Code prêt pour hébergement GitHub privé
- [x] Structure de projet complète

### 2. **Environnement & dépendances** ✅
- [x] Python ≥ 3.6 supporté (utilise Python 3.11)
- [x] Flask ≥ 1.11 dans `requirements.txt`
- [x] Peewee ORM configuré
- [x] RQ (Redis Queue) intégré
- [x] Installation via `pip install -r requirements.txt`

### 3. **Base de données PostgreSQL v12** ✅
- [x] Connexion via variables d'environnement (DB_HOST, DB_USER, etc.)
- [x] Initialisation via `flask init-db`
- [x] Modèles Peewee (Product, Order, OrderProduct)

### 4. **Cache & tâches asynchrones** ✅
- [x] Connexion Redis via `REDIS_URL`
- [x] PUT /order/<id> avec credit_card → 202 Accepted + job RQ
- [x] Worker RQ traite paiements en background
- [x] Cache Redis pour commandes avec flags "en cours"/"payé"
- [x] GET /order/<id> : gestion statuts 200/202/409

### 5. **Routes API** ✅
- [x] POST /order : accepte `products: [{id, quantity}]` + rétrocompatibilité
- [x] GET /order/<int:id> : JSON complet (products, total_price, shipping_price)
- [x] PUT /order/<int:id> : mise à jour + paiement asynchrone

### 6. **Containerisation** ✅
- [x] Dockerfile avec Python, Flask, Peewee, RQ
- [x] docker-compose.yml :
  - [x] Service `db` : Postgres v12 (port 5432, volume persistant)
  - [x] Service `redis` : Redis v5 (port 6379)
  - [x] Service `api` : application Flask
  - [x] Service `worker` : worker RQ

### 7. **Front-end minimal** ✅
- [x] Interface HTML/JavaScript pour toutes les routes
- [x] Formulaires pour POST/PUT via Fetch API
- [x] Page de test accessible via GET /test

## 🧪 Comment Tester l'Application

### 🔥 Test Rapide (recommandé)

```bash
# 1. Démarrer avec Docker (le plus simple)
./start.sh

# 2. Attendre que tous les services soient prêts (30 secondes)
sleep 30

# 3. Ouvrir l'interface de test dans le navigateur
open http://localhost:5002/test

# 4. Valider automatiquement le fonctionnement
./validate.sh
```

### 📋 Tests Étape par Étape

#### **1. Test de l'Interface Web**
1. **Ouvrir** : http://localhost:5002/test
2. **Afficher les produits** : Cliquer sur "Afficher produits"
   - ✅ Doit afficher une liste JSON de 10 produits avec id, name, price, weight, etc.

#### **2. Test Session 1 - Produit Unique**
1. **Créer une commande** :
   - ID produit : `1`
   - Quantité : `2`
   - Cliquer "Créer"
   - ✅ Doit afficher "Commande créée #1"

2. **Consulter la commande** :
   - ID commande : `1`
   - Cliquer "Afficher"
   - ✅ Doit afficher les détails : produits, prix, poids, frais livraison

3. **Mettre à jour l'adresse** :
   - ID commande : `1`
   - Province : `QC - Québec (15% taxes)`
   - Adresse : `123 Rue Test`
   - Ville : `Saguenay`
   - Code postal : `G7H 5K1`
   - Cliquer "Mettre à jour"
   - ✅ Doit recalculer les taxes automatiquement

4. **Payer la commande** :
   - ID commande : `1`
   - Nom : `John Doe`
   - Numéro carte : `4242 4242 4242 4242`
   - Expiration : `12/2025`
   - CVV : `123`
   - Cliquer "Payer"
   - ✅ Doit afficher "Paiement en cours..." (statut 202)

5. **Vérifier le paiement** :
   - Attendre 5-10 secondes
   - Consulter à nouveau la commande #1
   - ✅ Doit afficher "Payée : Oui"

#### **3. Test Session 2 - Multi-produits**
1. **Créer commande multi-produits** :
   - Produit 1 : ID `2`, Quantité `1`
   - Cliquer "+ Ajouter un produit"
   - Produit 2 : ID `3`, Quantité `2`
   - Cliquer "Créer"
   - ✅ Doit créer une commande avec 2 produits différents

2. **Tester les calculs complexes** :
   - Ajouter adresse avec province `ON` (Ontario 13%)
   - ✅ Vérifier que les taxes sont appliquées correctement
   - ✅ Vérifier que les frais de livraison dépendent du poids total

#### **4. Tests d'Erreur**
1. **Produit inexistant** :
   - ID produit : `999`
   - ✅ Doit afficher "Produit 999 introuvable"

2. **Quantité invalide** :
   - Quantité : `0` ou `-1`
   - ✅ Doit afficher "Quantité invalide"

3. **Carte de crédit invalide** :
   - Numéro : `1234`
   - ✅ Doit afficher "Numéro de carte invalide"

4. **Double paiement** :
   - Essayer de payer une commande déjà payée
   - ✅ Doit afficher "Cette commande est déjà payée!" (statut 409)

### 🔧 Tests API Directs (optionnel)

#### **Test avec curl**
```bash
# 1. Lister les produits
curl -X GET http://localhost:5002/api/products

# 2. Créer une commande (Session 1)
curl -X POST http://localhost:5002/order \
  -H "Content-Type: application/json" \
  -d '{"product": {"id": 1, "quantity": 2}}'

# 3. Créer une commande (Session 2)
curl -X POST http://localhost:5002/order \
  -H "Content-Type: application/json" \
  -d '{"products": [{"id": 1, "quantity": 2}, {"id": 3, "quantity": 1}]}'

# 4. Consulter une commande
curl -X GET http://localhost:5002/order/1

# 5. Mettre à jour une commande
curl -X PUT http://localhost:5002/order/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "shipping_information": {"province": "QC", "address": "123 Rue Test", "city": "Saguenay", "postal_code": "G7H 5K1"}}'

# 6. Payer une commande
curl -X PUT http://localhost:5002/order/1 \
  -H "Content-Type: application/json" \
  -d '{"credit_card": {"name": "John Doe", "number": "4242424242424242", "expiration_month": 12, "expiration_year": 2025, "cvv": "123"}}'
```

### 🚦 Validation Automatique

```bash
# Script de validation complet
./validate.sh

# Test de santé rapide
curl -f http://localhost:5002/api/products > /dev/null && echo "✅ API accessible" || echo "❌ API inaccessible"

# Vérifier les logs pour erreurs
docker-compose logs api | grep -i error
docker-compose logs worker | grep -i error
```

### 🐛 Diagnostic des Problèmes

#### **L'interface ne se charge pas**
```bash
# Vérifier que les services fonctionnent
docker-compose ps

# Vérifier les logs
docker-compose logs api
```

#### **Base de données vide**
```bash
# Réinitialiser la base
docker-compose exec api flask init-db
```

#### **Paiements qui ne se traitent pas**
```bash
# Vérifier le worker Redis
docker-compose logs worker

# Redémarrer le worker si nécessaire
docker-compose restart worker
```

#### **Port 5002 occupé**
```bash
# Changer le port dans docker-compose.yml
# ou arrêter le processus qui utilise le port
lsof -ti:5002 | xargs kill
```

### 📊 Résultats Attendus

#### **Calculs de Taxes (Session 1)**
- **Québec (QC)** : 15% sur le prix des produits uniquement
- **Ontario (ON)** : 13% sur le prix des produits uniquement
- **Alberta (AB)** : 5% sur le prix des produits uniquement

#### **Frais de Livraison**
- **≤ 500g** : 5,00 CAD
- **501-2000g** : 10,00 CAD  
- **> 2000g** : 25,00 CAD

#### **Exemple Complet**
```
Produit: 20,00$ × 2 = 40,00$ (300g × 2 = 600g)
Frais livraison: 600g → 10,00$
Taxes QC (15%): 40,00$ × 1.15 = 46,00$
TOTAL FINAL: 46,00$ + 10,00$ = 56,00$
```

## 🚀 Commandes de démarrage

### Démarrage rapide avec Docker
```bash
# 1. Démarrer l'application
./start.sh

# 2. Accéder à l'interface de test
open http://localhost:5002/test

# 3. Valider le fonctionnement
./validate.sh

# 4. Arrêter l'application
./stop.sh
```

### Démarrage manuel avec Docker Compose
```bash
# Démarrer tous les services
docker-compose up -d --build

# Initialiser la base de données
docker-compose exec api flask init-db

# Voir les logs
docker-compose logs -f api
docker-compose logs -f worker

# Arrêter
docker-compose down
```

### Développement local
```bash
# Installer les dépendances
pip install -r requirements.txt

# Variables d'environnement (créer un .env)
export FLASK_APP=app.py
export FLASK_ENV=development
export DB_HOST=localhost
export DB_USER=user
export DB_PASSWORD=pass
export DB_PORT=5432
export DB_NAME=api8inf349
export REDIS_URL=redis://localhost:6379

# Lancer l'application
python app.py

# Lancer le worker (autre terminal)
flask worker
```

## 🔧 Environnement de développement

### Installation des dépendances

1. **Créer un environnement virtuel** :
```bash
python3 -m venv .venv
```

2. **Activer l'environnement** :
```bash
# Sur macOS/Linux
source .venv/bin/activate

# Ou utiliser le script d'activation
source activate.sh
```

3. **Installer les dépendances** :
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Variables d'environnement
````markdown
# Exemple de variables d'environnement pour le développement
export FLASK_APP=app.py
export FLASK_ENV=development
export DB_HOST=localhost
export DB_USER=user
export DB_PASSWORD=pass
export DB_PORT=5432
export DB_NAME=api8inf349
export REDIS_URL=redis://localhost:6379
````

## 🧪 Tests de l'API

### Via interface web
- Ouvrir : http://localhost:5002/test
- Utiliser les formulaires pour tester toutes les fonctionnalités

### Via curl
```bash
# 1. Lister les produits
curl http://localhost:5002/api/products

# 2. Créer une commande
curl -X POST http://localhost:5002/order \
  -H "Content-Type: application/json" \
  -d '{"products": [{"id": 1, "quantity": 2}]}'

# 3. Consulter une commande
curl http://localhost:5002/order/1

# 4. Payer une commande (asynchrone)
curl -X PUT http://localhost:5002/order/1 \
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
  }'
```

## 📁 Structure finale du projet

```
WebAvanc-es/
├── app.py                 # Point d'entrée Flask + commandes CLI
├── requirements.txt       # Dépendances Python
├── Dockerfile            # Image Docker de l'application
├── docker-compose.yml    # Services (db, redis, api, worker)
├── env.example          # Variables d'environnement exemple
├── CODES-PERMANENTS     # Codes permanents des membres
├── README.md            # Documentation complète
├── start.sh             # Script de démarrage rapide
├── stop.sh              # Script d'arrêt
├── validate.sh          # Script de validation/test
├── App/
│   ├── config.py        # Configuration de l'application
│   ├── models.py        # Modèles Peewee (Product, Order, OrderProduct)
│   ├── routes.py        # Routes de l'API Flask
│   ├── services.py      # Services (import produits, paiements RQ)
│   ├── redis_client.py  # Client Redis
│   └── worker.py        # Worker RQ pour tâches asynchrones
└── templates/
    └── index.html       # Interface de test HTML/JavaScript
```

## 🎉 L'application est maintenant prête !

- ✅ Tous les points des exigences sont respectés
- ✅ Code production-ready avec Docker
- ✅ Interface de test fonctionnelle
- ✅ Documentation complète
- ✅ Scripts de démarrage/validation inclus

### Prochaines étapes pour la mise en production :
1. Ajouter le repository à GitHub en privé
2. Inviter `jgnault@uqac.ca` comme collaborateur
3. Configurer les variables d'environnement de production
4. Déployer avec `docker-compose up -d --build`
