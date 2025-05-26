#!/bin/sh
# Installation des dépendances et lancement du serveur
set -e

SCRIPT_DIR="$(dirname "$0")"
pip install -r "$SCRIPT_DIR/requirements.txt"

# Lancer Uvicorn depuis la racine du repo pour ne pas surcharger Pydantic
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"
exec uvicorn packages.api.app.main:app --reload
