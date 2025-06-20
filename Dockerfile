# 1) Image de base
FROM python:3.11-slim

# 2) Création du dossier de travail dans le conteneur
WORKDIR /usr/src/app

# 3) Copier le fichier des dépendances puis les installer
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copier le reste du code dans le conteneur
COPY . .

# 5) Variables d'environnement pour Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 6) Exposition du port (l’application écoute sur 5000)
EXPOSE 5000

# 7) Commande par défaut pour lancer l’application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
