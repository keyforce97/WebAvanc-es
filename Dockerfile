#Image de base
FROM python:3.11-slim

#dossier de travail dans le conteneur
WORKDIR /usr/src/app

COPY requirements.txt ./           
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code 
COPY . .


# Variables d'environnement pour Flask
ENV FLASK_APP=api8inf349.py
ENV FLASK_ENV=production

#  Exposition du port (l'application écoute sur 5000)
EXPOSE 5000

# Commande par défaut pour lancer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api8inf349:app"]
