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
4. **Initialiser la base de données et importer les produits**
   > ⚠️ **Assure-toi d'avoir un service pour l'app dans `docker-compose.yml` (ex: `api`)**
   > et d'avoir copié `.env.example` en `.env` à la racine du projet.
   ```sh
   docker-compose run api flask init-db
   ```
5. **Lancer le worker (paiement en tâche de fond)**
   
   **Si tu utilises Docker :**
   ```sh
   docker run --env-file .env.example api8inf349 python App/worker.py
   ```
   **Si tu es en local (hors docker, Python et Redis installés) :**
   ```sh
   python App/worker.py
   ```
   > ⚠️ Si tu as une erreur d'import dans le worker, modifie `App/worker.py` :
   > Remplace `from rq.connections import Connection` par `from rq import Connection`.
   >
   > Le worker affiche des logs détaillés pour chaque paiement traité.

---

### Dépannage port déjà utilisé

Si tu as l'erreur :
```
Bind for 0.0.0.0:5002 failed: port is already allocated.
```
Cela veut dire qu'un autre conteneur utilise déjà ce port. Pour le libérer :
```sh
docker ps # repère l'ID du conteneur à arrêter
docker stop <container_id>
```
Ou pour tout nettoyer :
```sh
docker-compose down
```
Puis relance la commande docker run.

## Tester l'API
- Accédez à [http://localhost:5002/test](http://localhost:5002/test) pour une interface web simple.
- Les routes principales :
  - `GET /` : liste des produits
  - `POST /order` : créer une commande (plusieurs produits supportés)
  - `GET /order/<id>` : voir une commande
  - `PUT /order/<id>` : mettre à jour/payer une commande

## Fonctionnement du paiement
- Le paiement est asynchrone :
  - Quand tu paies une commande, la route retourne 202 "Paiement en cours...".
  - Le worker traite la tâche en fond (voir logs du worker pour le suivi).
  - Après quelques secondes, la commande passe à `paid: true`.
  - Rafraîchis la commande pour voir le statut mis à jour.

## Infos utiles
- Variables d'environnement à adapter dans `.env.example` puis copier dans `.env`.
- Les données Postgres sont conservées dans le volume `pgdata`.
- Fichier `CODES-PERMANENTS` à la racine avec votre code permanent.
- Dépendances : Flask, peewee, psycopg2-binary, redis, rq, etc.

## Dépannage
- Si le paiement ne passe jamais à `paid: true`, vérifie que le worker tourne bien et regarde ses logs.
- Redis doit être accessible (voir `REDIS_URL` dans `.env`).
- Pour plus de détails, consulte les logs du worker (affichés dans le terminal où il tourne).

## GitHub
- Déposez votre code sur GitHub et partagez le lien.
