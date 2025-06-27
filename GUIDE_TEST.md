# 🧪 Guide Complet de Test de l'API de Gestion de Commandes

## ⚠️ Exigences Obligatoires du Projet

### 🎯 Session 1 - Exigences Minimales
- ✅ **Base de données** : SQLite → **Migré vers PostgreSQL v12**
- ✅ **Format commande** : `{"product": {"id": 1, "quantity": 2}}` 
- ✅ **Paiement** : Synchrone → **Migré vers asynchrone (Session 2)**
- ✅ **Calculs** : Taxes selon province + frais livraison selon poids

### 🎯 Session 2 - Exigences Complètes (TOUTES OBLIGATOIRES)
- ✅ **Multi-produits** : `{"products": [{"id": 1, "quantity": 2}, {"id": 3, "quantity": 1}]}`
- ✅ **PostgreSQL v12** : Variables d'environnement (DB_HOST, DB_USER, etc.)
- ✅ **Redis** : Cache + gestion tâches asynchrones
- ✅ **Worker RQ** : Paiements traités en arrière-plan
- ✅ **Docker Compose** : Tous services containerisés
- ✅ **Statuts HTTP** : 202 (en cours), 409 (déjà payé), 422 (erreur)
- ✅ **Initialisation** : `flask init-db` + import produits

### 🚨 Contraintes Techniques Obligatoires
1. **Port 5002** : API doit être accessible sur localhost:5002
2. **4 Services Docker** : api, db (PostgreSQL), redis, worker
3. **Worker actif** : `docker-compose exec api rq worker default`
4. **Base initialisée** : `docker-compose exec api flask init-db`
5. **Aucune erreur** dans les logs des services

## 🚀 Démarrage Rapide

### 1. Lancer l'application
```bash
# ⚠️ IMPORTANT: Exigences du projet
# 1. Arrêter et nettoyer les anciens containers/volumes
docker-compose down -v

# 2. Construire et démarrer TOUS les services (obligatoire)
docker-compose up -d --build

# 3. OBLIGATOIRE: Initialiser la base de données
docker-compose exec api flask init-db

# 4. OBLIGATOIRE: Démarrer le worker RQ (session 2)
# Dans un terminal séparé:
docker-compose exec api rq worker default

# 5. Attendre que tous les services soient prêts
sleep 30

# 6. Ouvrir l'interface de test
open http://localhost:5002/test
```

### ⚠️ Exigences Critiques du Projet
- **PostgreSQL v12** : Base de données obligatoire (pas SQLite)
- **Redis** : Cache et gestion des tâches asynchrones
- **Worker RQ** : Traitement des paiements en arrière-plan
- **Initialisation BD** : `flask init-db` OBLIGATOIRE avant tests
- **Port 5002** : API accessible sur localhost:5002 (pas 5000)
- **Docker Compose** : Tous les services doivent être opérationnels

### 2. Validation automatique
```bash
# 🎯 NOUVEAU: Vérification complète des exigences
./check_requirements.sh

# ⚠️ IMPORTANT: Vérifier que TOUS les services sont opérationnels
docker-compose ps

# Tous les services doivent être "Up":
# - db (PostgreSQL)
# - api (Flask) 
# - redis (Cache)
# - worker (RQ)

# Script de validation complet
./validate.sh

# Tests API automatiques
./test_api.sh
```

### 🔧 Vérifications Obligatoires Avant Tests
```bash
# 1. Vérifier les containers
docker-compose ps

# 2. Vérifier les logs (pas d'erreurs)
docker-compose logs api
docker-compose logs worker
docker-compose logs db

# 3. Tester la connectivité PostgreSQL
docker-compose exec db psql -U user -d api8inf349 -c "SELECT version();"

# 4. Tester Redis
docker-compose exec redis redis-cli ping

# 5. Vérifier que les produits sont importés
curl -s http://localhost:5002/api/products | head -5
```

## 🖥️ Tests via Interface Web

### Étape 1: Vérifier l'accès
- **URL**: http://localhost:5002/test
- **Vérification**: La page doit s'afficher avec les sections de test

### Étape 2: Tester les produits
1. Cliquer sur **"Afficher produits"**
2. **Résultat attendu**: JSON avec 10 produits
3. **Vérifier**: Chaque produit a `id`, `name`, `price`, `weight`, `in_stock`
4. **Exemples de poids réels**:
   - Produit 1 (Brown eggs): 400g
   - Produit 2 (Sweet fresh strawberry): 299g
   - Produit 3 (Butter): 227g
   - Produit 4 (Honey): 340g

### Étape 3: Test Session 1 (Produit unique)
1. **Créer une commande**:
   - ID produit: `1`
   - Quantité: `2`
   - Cliquer "Créer"
   - **Attendu**: "Commande créée #1"

2. **Consulter la commande**:
   - ID commande: `1`
   - Cliquer "Afficher"
   - **Attendu**: Détails avec prix, poids, frais livraison

3. **Ajouter une adresse**:
   - ID commande: `1`
   - Email: `test@example.com`
   - Province: `QC - Québec (15% taxes)`
   - Adresse: `123 Rue Test`
   - Ville: `Saguenay`
   - Code postal: `G7H 5K1`
   - Cliquer "Mettre à jour"
   - **Attendu**: Message avec recalcul des taxes

4. **Payer la commande**:
   - ID commande: `1`
   - Nom: `John Doe`
   - Numéro: `4242 4242 4242 4242`
   - Expiration: `12/2025`
   - CVV: `123`
   - Cliquer "Payer"
   - **Attendu**: "Paiement en cours..." (202)

5. **Vérifier le paiement**:
   - Attendre 10 secondes
   - Consulter à nouveau la commande #1
   - **Attendu**: "Payée : Oui"

### Étape 4: Test Session 2 (Multi-produits)
1. **Créer commande multi-produits**:
   - Produit 1: ID `2`, Quantité `1`
   - Cliquer "+ Ajouter un produit"
   - Produit 2: ID `3`, Quantité `2`
   - Cliquer "Créer"
   - **Attendu**: Commande avec 2 produits

2. **Tester calculs complexes**:
   - Ajouter adresse Ontario (`ON`)
   - **Attendu**: Taxes 13% + frais livraison selon poids total

### Étape 5: Tests Spécifiques aux Poids
1. **Test poids léger (≤500g)**:
   - Créer commande: Produit 2 (Strawberry 299g) × 1
   - **Attendu**: Frais livraison 5,00$ CAD

2. **Test poids moyen (501-2000g)**:
   - Créer commande: Produit 1 (Brown eggs 400g) × 2 = 800g
   - **Attendu**: Frais livraison 10,00$ CAD

3. **Test poids lourd (>2000g)**:
   - Créer commande: Produit 1 (Brown eggs 400g) × 6 = 2400g
   - **Attendu**: Frais livraison 25,00$ CAD

4. **Test multi-produits avec calcul poids**:
   - Produit 1 (400g) × 2 + Produit 2 (299g) × 1 = 1099g
   - **Attendu**: Frais livraison 10,00$ CAD (tranche 501-2000g)

### Étape 6: Tests d'erreur
1. **Produit inexistant**: ID `999` → "Produit 999 introuvable"
2. **Quantité invalide**: `0` → "Quantité invalide"
3. **Carte invalide**: `1234` → "Numéro de carte invalide"
4. **Double paiement**: Payer une commande payée → "Déjà payée!"

## 🔧 Tests API Directs (curl)

### Configuration
```bash
export API_URL="http://localhost:5002"
```

### Tests de base
```bash
# 1. Lister les produits (voir les poids)
curl -X GET $API_URL/api/products

# 2. Créer commande Session 1
curl -X POST $API_URL/order \
  -H "Content-Type: application/json" \
  -d '{"product": {"id": 1, "quantity": 2}}'

# 3. Créer commande Session 2
curl -X POST $API_URL/order \
  -H "Content-Type: application/json" \
  -d '{"products": [{"id": 1, "quantity": 2}, {"id": 3, "quantity": 1}]}'

# 4. Test poids léger (≤500g) - Strawberry 299g × 1
curl -X POST $API_URL/order \
  -H "Content-Type: application/json" \
  -d '{"products": [{"id": 2, "quantity": 1}]}'

# 5. Test poids moyen (501-2000g) - Brown eggs 400g × 2 = 800g
curl -X POST $API_URL/order \
  -H "Content-Type: application/json" \
  -d '{"products": [{"id": 1, "quantity": 2}]}'

# 6. Test poids lourd (>2000g) - Brown eggs 400g × 6 = 2400g
curl -X POST $API_URL/order \
  -H "Content-Type: application/json" \
  -d '{"products": [{"id": 1, "quantity": 6}]}'

# 7. Consulter commande (voir calculs de poids)
curl -X GET $API_URL/order/1

# 5. Mettre à jour adresse
curl -X PUT $API_URL/order/1 \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "shipping_information": {
      "province": "QC",
      "address": "123 Rue Test",
      "city": "Saguenay",
      "postal_code": "G7H 5K1"
    }
  }'

# 6. Payer
curl -X PUT $API_URL/order/1 \
  -H "Content-Type: application/json" \
  -d '{
    "credit_card": {
      "name": "John Doe",
      "number": "4242424242424242",
      "expiration_month": 12,
      "expiration_year": 2025,
      "cvv": "123"
    }
  }'
```

## 📊 Résultats Attendus

### Calculs de Taxes
- **QC (Québec)**: 15% sur prix produits
- **ON (Ontario)**: 13% sur prix produits  
- **AB (Alberta)**: 5% sur prix produits
- **Autres**: 0% (non configuré)

### Frais de Livraison
- **≤ 500g**: 5,00 CAD
- **501-2000g**: 10,00 CAD
- **> 2000g**: 25,00 CAD

**Formule**: `total_weight = Σ(product.weight × quantity)`

### Exemple Complet
```
Produit 1 (Brown eggs): 28,10$ × 2 = 56,20$ (400g × 2 = 800g)
Frais livraison: 800g → 10,00$ (dans tranche 501-2000g)
Taxes QC (15%): 56,20$ × 1.15 = 64,63$ TTC
TOTAL FINAL: 64,63$ + 10,00$ = 74,63$ CAD
```

### Exemples avec Différents Poids
```
🥚 Produit 1 (Brown eggs - 400g):
   × 1 = 400g → Livraison 5,00$ (≤500g)
   × 2 = 800g → Livraison 10,00$ (501-2000g)
   × 6 = 2400g → Livraison 25,00$ (>2000g)

🍓 Produit 2 (Strawberry - 299g):
   × 1 = 299g → Livraison 5,00$ (≤500g)
   × 2 = 598g → Livraison 10,00$ (501-2000g)
   × 7 = 2093g → Livraison 25,00$ (>2000g)

🧈 Multi-produits:
   2× Brown eggs (800g) + 1× Strawberry (299g) = 1099g
   → Livraison 10,00$ (501-2000g)
```

### Codes de Retour
- **200**: Succès
- **302**: Redirection après création
- **202**: Paiement en cours (asynchrone)
- **409**: Commande déjà payée
- **422**: Erreur de validation
- **404**: Commande introuvable

## 🐛 Diagnostic

### ❌ Erreurs Courantes et Solutions

#### **"Connection refused" ou API inaccessible**
```bash
# Vérifier que TOUS les services sont "Up"
docker-compose ps

# Si des services sont "Exit" ou manquants:
docker-compose down -v
docker-compose up -d --build
```

#### **"Base de données vide" ou "Table doesn't exist"**
```bash
# OBLIGATOIRE après chaque redémarrage
docker-compose exec api flask init-db

# Vérifier que les tables existent
docker-compose exec db psql -U user -d api8inf349 -c "\dt"
```

#### **Paiements qui ne se traitent jamais (restent en 202)**
```bash
# Le worker RQ DOIT être démarré manuellement
docker-compose exec api rq worker default

# Dans un terminal séparé, laisser tourner en permanence
```

#### **"Redis connection failed"**
```bash
# Vérifier Redis
docker-compose exec redis redis-cli ping
# Doit retourner "PONG"

# Si échec, redémarrer Redis
docker-compose restart redis
```

### Services qui ne démarrent pas
```bash
# Vérifier l'état des conteneurs
docker-compose ps

# Voir les logs
docker-compose logs api
docker-compose logs worker
docker-compose logs db
docker-compose logs redis

# Redémarrer un service
docker-compose restart api
```

### Base de données vide
```bash
# Réinitialiser
docker-compose exec api flask init-db

# Vérifier les tables
docker-compose exec db psql -U user -d api8inf349 -c "\dt"
```

### Problèmes de paiement
```bash
# Vérifier le worker Redis
docker-compose logs worker

# Vérifier Redis
docker-compose exec redis redis-cli ping

# Redémarrer le worker
docker-compose restart worker
```

### Port occupé
```bash
# Trouver ce qui utilise le port 5002
lsof -ti:5002

# Tuer le processus
lsof -ti:5002 | xargs kill

# Ou changer le port dans docker-compose.yml
```

## 🎯 Checklist de Validation

### ✅ Fonctionnalités Core
- [ ] API accessible (GET /api/products)
- [ ] Création commande produit unique (Session 1)
- [ ] Création commande multi-produits (Session 2)
- [ ] Consultation commande (GET /order/id)
- [ ] Mise à jour adresse + calcul taxes
- [ ] Paiement asynchrone (statut 202)
- [ ] Vérification paiement traité

### ✅ Calculs Métier
- [ ] Frais livraison selon poids total (Σ(weight × quantity))
- [ ] Poids calculé correctement pour multi-produits
- [ ] Seuils de poids respectés (500g, 2000g)
- [ ] Taxes selon province (QC 15%, ON 13%, AB 5%)
- [ ] Taxes appliquées aux produits uniquement
- [ ] Recalcul automatique lors mise à jour

### ✅ Gestion d'Erreurs
- [ ] Produit inexistant (422)
- [ ] Quantité invalide (422)
- [ ] Carte de crédit invalide (422)
- [ ] Double paiement (409)
- [ ] Commande introuvable (404)

### ✅ Interface Web
- [ ] Formulaires fonctionnels
- [ ] Validation côté client
- [ ] Messages d'erreur clairs
- [ ] Affichage détaillé des calculs

### ✅ Architecture
- [ ] Docker containers opérationnels (docker-compose ps)
- [ ] PostgreSQL v12 connecté et initialisé
- [ ] Redis opérationnel (redis-cli ping)
- [ ] Worker RQ démarré et en attente
- [ ] Flask init-db exécuté avec succès
- [ ] Produits importés depuis l'API externe
- [ ] Cache Redis pour commandes payées
- [ ] Port 5002 accessible (pas de conflit)
- [ ] Variables d'environnement correctes
- [ ] Volumes Docker persistants

## 🏆 Tests de Performance

### Tests de Poids et Calculs
```bash
# Test avec différents poids pour vérifier les calculs
echo "🧪 Test calculs de poids et frais de livraison"

# Poids léger (≤500g)
echo "Test 1: Poids léger"
curl -X POST http://localhost:5002/order \
  -H "Content-Type: application/json" \
  -d '{"products": [{"id": 2, "quantity": 1}]}' # Strawberry 299g

# Poids moyen (501-2000g)  
echo "Test 2: Poids moyen"
curl -X POST http://localhost:5002/order \
  -H "Content-Type: application/json" \
  -d '{"products": [{"id": 1, "quantity": 2}]}' # Brown eggs 800g

# Poids lourd (>2000g)
echo "Test 3: Poids lourd"
curl -X POST http://localhost:5002/order \
  -H "Content-Type: application/json" \
  -d '{"products": [{"id": 1, "quantity": 6}]}' # Brown eggs 2400g
```

### Charge
```bash
# Test de charge avec Apache Bench
ab -n 100 -c 10 http://localhost:5002/api/products

# Test de création de commandes
for i in {1..10}; do
  curl -X POST http://localhost:5002/order \
    -H "Content-Type: application/json" \
    -d '{"products": [{"id": 1, "quantity": 2}]}'
done
```

### Monitoring
```bash
# Utilisation CPU/RAM
docker stats

# Logs en temps réel
docker-compose logs -f api worker
```

## 📚 Ressources

- **Documentation**: `README.md` et `QUICK_START.md`
- **Scripts**: `start.sh`, `stop.sh`, `validate.sh`, `test_api.sh`
- **Interface**: http://localhost:5002/test
- **Logs**: `docker-compose logs`
