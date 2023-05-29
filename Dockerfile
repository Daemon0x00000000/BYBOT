# Image de base
FROM python:3.10-slim-buster

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers de l'application
COPY . /app

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Définition des variables d'environnement Flask
ENV FLASK_ENV=production

# Exposition du port 8000
EXPOSE 8000

# Démarrage de l'application
CMD ["python", "main.py"]
