#!/bin/sh
# Installation des dépendances et lancement du serveur
set -e
pip install -r requirements.txt
exec uvicorn app.main:app --reload
