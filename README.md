# Coaching App

Cette application fournit une base pour un outil de suivi sportif. Elle s'adresse
à un athlète vétéran multisports et se compose d'un backend FastAPI et d'un
frontend React simple.

## Backend
- Python / FastAPI
- Endpoints principaux :
  - `GET /health` : vérifie que l'API fonctionne.
- `GET /sessions` : liste des séances enregistrées.
- `POST /sessions` : enregistre une nouvelle séance.
- `GET /sessions/today` : renvoie les séances prévues pour aujourd'hui.
- `PUT /sessions/{id}` : met à jour une séance.
- `GET /stats/acwr` : calcule le ratio de charge d'entraînement (ACWR).
- Les modèles sont définis dans `backend/app/models.py` et les données sont
  stockées dans une base en mémoire (`backend/app/db.py`).

## Frontend
- React (structure minimaliste)
- Fichiers dans le répertoire `frontend`

Ce projet est volontairement simple et sert de point de départ pour
étendre l'application vers les nombreuses fonctionnalités décrites dans le
cahier des charges.

## Tests

`pytest` doit être installé (voir `backend/requirements.txt`).

```
pip install -r backend/requirements.txt
pytest
```

## Plan d'évolution

Les étapes détaillées pour transformer ce prototype en application complète
sont décrites dans [PLAN.md](PLAN.md).
