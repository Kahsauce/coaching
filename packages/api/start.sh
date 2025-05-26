#!/bin/sh
# Installation des dépendances et lancement du serveur
set -e
# Tente d'installer les dépendances mais n'échoue pas si le réseau est indisponible
pip install -r requirements.txt >/tmp/pip.log 2>&1 || echo "Dépendances déjà installées ou réseau indisponible"
exec uvicorn app.main:app --reload
