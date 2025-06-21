# Projet API Commandes (Flask, PostgreSQL, Redis, Docker)

## Lancer le projet rapidement

1. **Démarrer les services Postgres & Redis**
   ```sh
   docker-compose up -d
   ```
   # docker-compose down  
2. **Construire l'image de l'app**
   ```sh
   docker build -t api8inf349 .
   ```
3. **Lancer l'application Flask**
   ```sh
   docker run --env-file .env.example -p 5002:5000 api8inf349
   # Le port 5002 de votre machine sera redirigé vers le port 5000 du conteneur (Flask écoute sur 5000).
   # Accédez à l'application sur http://localhost:5002
   ```
4. **Initialiser la base de données**
   > ⚠️ **Assure-toi d'avoir un service pour l'app dans `docker-compose.yml` (ex: `api`)**
   > et d'avoir copié `.env.example` en `.env` à la racine du projet.
   ```sh
   docker-compose run api flask init-db
   ```
5. **Lancer le worker (paiement en tâche de fond)**
   ```sh
   docker run --env-file .env.example api8inf349 python App/worker.py
   ```
## Tester l'API
- Accédez à [http://localhost:5002/test](http://localhost:5002/test) pour une interface web simple.
- Les routes principales :
  - `GET /` : liste des produits
  - `POST /order` : créer une commande (plusieurs produits supportés)
  - `GET /order/<id>` : voir une commande
  - `PUT /order/<id>` : mettre à jour/payer une commande

## Infos utiles
- Variables d'environnement à adapter dans `.env.example` puis copier dans `.env`.
- Les données Postgres sont conservées dans le volume `pgdata`.
- Fichier `CODES-PERMANENTS` à la racine avec votre code permanent.
- Dépendances : Flask, peewee, psycopg2-binary, redis, rq, etc.

## GitHub
- Déposez votre code sur GitHub et partagez le lien.
