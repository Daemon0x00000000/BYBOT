import secrets
import sys

from dotenv import load_dotenv
import os
from _server import app


def main():
    load_dotenv()
    sys.stdout.write("""

     .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
    | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
    | | _____  _____ | || |  ____  ____  | || |              | || |    _______   | || |  _________   | || |  _______     | || |      __      | || |   ______     | || |     ____     | || |  _________   | |
    | ||_   _||_   _|| || | |_   ||   _| | || |              | || |   /  ___  |  | || | |  _   _  |  | || | |_   __ \    | || |     /  \     | || |  |_   _ \    | || |   .'    `.   | || | |  _   _  |  | |
    | |  | | /\ | |  | || |   | |__| |   | || |              | || |  |  (__ \_|  | || | |_/ | | \_|  | || |   | |__) |   | || |    / /\ \    | || |    | |_) |   | || |  /  .--.  \  | || | |_/ | | \_|  | |
    | |  | |/  \| |  | || |   |  __  |   | || |              | || |   '.___`-.   | || |     | |      | || |   |  __ /    | || |   / ____ \   | || |    |  __'.   | || |  | |    | |  | || |     | |      | |
    | |  |   /\   |  | || |  _| |  | |_  | || |              | || |  |`\____) |  | || |    _| |_     | || |  _| |  \ \_  | || | _/ /    \ \_ | || |   _| |__) |  | || |  \  `--'  /  | || |    _| |_     | |
    | |  |__/  \__|  | || | |____||____| | || |   _______    | || |  |_______.'  | || |   |_____|    | || | |____| |___| | || ||____|  |____|| || |  |_______/   | || |   `.____.'   | || |   |_____|    | |
    | |              | || |              | || |  |_______|   | || |              | || |              | || |              | || |              | || |              | || |              | || |              | |
    | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
     '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 

    """)

    # Check if environment variable PRIVATE_TOKEN is set and is valid
    if os.getenv('PRIVATE_TOKEN') is None or len(os.getenv('PRIVATE_TOKEN')) != 43:
        print("Génération du token privé...")
        generatePrivateToken()
    os.system('gunicorn --worker-class=gevent --worker-connections=1000 --workers=5 --bind=0.0.0.0:8000 main:app')


def generatePrivateToken():
    token = secrets.token_urlsafe(32)
    # Store it in env variable, if PRIVATE_TOKEN is already set, replace it
    with open('.env', 'r') as f:
        lines = f.readlines()
    with open('.env', 'w') as f:
        replace = False
        for line in lines:
            if line.startswith('PRIVATE_TOKEN'):
                f.write(f"PRIVATE_TOKEN={token}")
                replace = True
            else:
                f.write(line)
        if not replace:
            f.write(f"PRIVATE_TOKEN={token}")
    print("Token privé : " + token)
    print("Le token privé a été enregistré dans le fichier .env (à ne pas partager !)")


if __name__ == '__main__':
    main()
