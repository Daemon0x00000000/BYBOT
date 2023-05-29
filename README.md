# ByBOT

Ce projet est un bot Python qui utilise Flask pour créer une API web permettant d'exécuter des actions de trading sur la plateforme Bybit. Le bot convertit les signaux reçus via des requêtes POST en ouvertures de positions (long, short) ou en fermetures (flat) sur Bybit. Il envoie également des messages via Telegram pour tenir les utilisateurs informés des actions du bot.

## Environnement de production

Ce projet utilise l’interface WSGI, par défaut il utilise Gunicorn mais vous pouvez très bien configurer Apache de sorte à ce qu’il communique avec Flask.

## Fonctionnalités

- Réception des signaux de trading via des requêtes POST avec authentification par token privé.
- Conversion des signaux en actions de trading sur Bybit.
- Envoi de messages Telegram pour informer des actions du bot.
- Gestion de multiples stratégies de trading via des configurations spécifiques dans le fichier `config.json`.
- Conteneurisation de l'application pour faciliter le déploiement.

## Installation

1. Clonez ce dépôt :

   ```shell
   git clone https://github.com/votre-utilisateur/mon-projet.git
   ```
2. Accédez au dossier du projet :
   
   ```shell
    cd mon-projet
    ```
3. Installez les dépendances si vous n'utilisez pas Docker:
    
    ```shell
     pip install -r requirements.txt
     ```
   
## Configuration
1. Créer un fihcier `.env` à la racine du projet et ajoutez les informations suivantes :
    
    ```shell
    ASSET=YOUR_ASSET
    TELEGRAM_TOKEN=token_telegram
    TELEGRAM_CHAT_ID=chat_id_telegram
    ```
2. Créer un fichier `config.json` à la racine du projet et ajoutez les informations suivantes :
    
    ```shell
    {
      "YOUR_STRATEGY_NAME": {
         "API_KEY": "YOUR_API_KEY",
         "API_SECRET": "YOUR_API_SECRET"
      }
    }
    ```

## Utilisation

### Avec Docker

1. Construisez l'image Docker :

   ```shell
   docker build -t bybot .
   ```
2. Lancez le conteneur :

   ```shell
   docker run -d -p 80:8000 -v /srv/appdata/strabot/.env:/app/.env -v /srv/appdata/strabot/config.json:/app/config.json --name bybot bybot
   ```
3.Accédez à l'application via l'adresse `http://localhost'

### Sans Docker
1. Lancez l'application :
   
   ```shell
   python main.py
   ```
 2. Accédez à l'application via l'adresse `http://localhost:8000'

## Prochainement

L’implémentation de CCXT Pro avec l’extension à d’autres plateformes de trading est prévue prochainement.

Le bot pourra prochainement enregistrer les données directement dans une BDD et bénéficiera d’une interface web pour le suivi des trades effectuées par le bot.