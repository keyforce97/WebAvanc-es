# README

Ce projet implémente une API Flask pour la gestion de commandes, avec traitement asynchrone des paiements via RQ et stockage Postgres.

## Prérequis

* Docker & Docker Compose (version 2.x)
* Python 3.11 (pour l'environnement virtuel)
* \[Optionnel] `python-dotenv` si vous souhaitez charger automatiquement le `.env`

## Structure du projet

```
├── App/
│   ├── models.py       # Modèles Peewee
│   ├── routes.py       # Définitions des endpoints Flask
│   ├── services.py     # Logique métier (ex : process_payment)
│   └── worker.py       # Script de démarrage du worker RQ
├── docker-compose.yml  # Définition des services (api, db, redis)
├── Dockerfile          # Construction de l'image API
├── requirements.txt    # Dépendances Python
├── .env.example        # Exemple de variables d'environnement
└── README.md           # Ce fichier
```

## Lancement des services

À la racine du projet :

```bash
# Arrête et supprime conteneurs + volumes
docker-compose down -v

# Reconstruit et démarre les services en arrière-plan
docker-compose up -d --build

# Initialise la base de données et importe les produits
docker-compose exec api flask init-db
```

* L'API sera disponible sur `http://localhost:5002` # (port5002)ou 5000 à vous de choisir.
* PostgreSQL sur le port `5432`
* Redis sur le port `6379`

## Exécution du Worker RQ

Ouvrez un nouveau terminal :

```bash
docker-compose exec api rq worker default
```
Le worker attendra les jobs de paiement en file.




-------------




## Tests

Suivez ces instructions pas-à‑pas, dans **trois terminaux séparés** :

### Terminal 1 : Logs de l’API

```bash
cd ~/Documents/WebAvanc-es
# Vérifier que les services tournent
docker-compose ps
# Suivre les logs de l'API
docker-compose logs -f api
```

### Terminal 2 : Worker RQ

```bash
cd ~/Documents/WebAvanc-es
docker-compose exec api rq worker default
```

### Terminal 3 : Tester les endpoints avec `curl`

1. **Créer une commande** :

   ```bash
   curl -i -X POST http://localhost:5002/order \
     -H "Content-Type: application/json" \
     -d '{"products":[{"id":2,"quantity":1}]}'
   ```

   → Notez le `<order_id>` renvoyé dans le header `Location: /order/<order_id>`.

2. **Consulter la commande (non payée)** :

   ```bash
   curl -i http://localhost:5002/order/<order_id>
   ```

   → Vous devez voir `"paid":false`.

3. **Envoyer le paiement** :

   ```bash
   curl -i -X PUT http://localhost:5002/order/<order_id> \
     -H "Content-Type: application/json" \
     -d '{
           "credit_card": {
             "name": "John Doe",
             "number": "4242424242424242",
             "expiration_year": 2024,
             "expiration_month": 9,
             "cvv": "123"
           }
         }'
   ```

   → Vous devez recevoir **202 Accepted**.

4. **Observer le traitement** dans le Terminal 2 (worker) :

   ```
   Processing order <order_id>…
   Payment successful for order <order_id>
   ```

5. **Vérifier la commande (payée)** :

   ```bash
   curl -i http://localhost:5002/order/<order_id>
   ```

   → Cette fois, `"paid":true` et l’objet `"transaction"` est rempli.

## Bonus : Tester les produits disponibles

Pour lister tous les produits et vérifier leur stock :

```bash
curl -s http://localhost:5002/ | python -m json.tool
```

Repérez les `id` dont `"in_stock":true` pour les utiliser dans vos tests.


