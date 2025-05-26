# Coaching App

Cette application fournit une base pour un outil de suivi sportif. Elle s'adresse
à un athlète vétéran multisports et est désormais organisée en **monorepo** grâce à
Turborepo.

La structure principale est la suivante :

- `apps/web` : frontend React
- `apps/mobile` : première version mobile réalisée avec React Native
- `packages/api` : backend FastAPI

## Démarrage rapide

```bash
./start.sh
```

Le script démarre l'API et l'interface web. Le frontend est ensuite
accessible sur `http://localhost:3000`.

La liste complète des endpoints est présentée dans [docs/api.md](docs/api.md).

## Backend
- Python / FastAPI
- Endpoints principaux :
  - `GET /health` : vérifie que l'API fonctionne.
- `GET /sessions` : liste des séances enregistrées.
- `POST /sessions` : enregistre une nouvelle séance.
- `GET /sessions/today` : renvoie les séances prévues pour aujourd'hui.
- `GET /sessions/week` : renvoie les séances de la semaine en cours.
- `PUT /sessions/{id}` : met à jour une séance.
- `GET /stats/acwr` : calcule le ratio de charge d'entraînement (ACWR).
- `GET /stats/summary` : ACWR, charges hebdo et progression.
- `POST /nutrition/plan` : génère un plan nutrition basé sur le poids et l'objectif.
- Les modèles sont définis dans `packages/api/app/models.py` et les données sont
  désormais persistées dans SQLite (`coaching.db`). On peut choisir un autre
  backend via la variable d'environnement `COACHING_DB`.

## Frontend
- React (structure minimaliste)
- Fichiers dans le répertoire `apps/web`
- Pages disponibles : tableau de bord "Aujourd'hui" et calendrier hebdomadaire.

Ce projet est volontairement simple et sert de point de départ pour
étendre l'application vers les nombreuses fonctionnalités décrites dans le
cahier des charges.

## Tests

`pytest` doit être installé (voir `packages/api/requirements.txt`). Les entrées
de nutrition permettent désormais de renseigner les macronutriments (glucides,
protéines, lipides). Une action GitHub exécute automatiquement ces tests à
chaque pull request.

```
pip install -r packages/api/requirements.txt
pytest --cov=packages/api/app --cov-report=term-missing
```

## Plan d'évolution

Les étapes détaillées pour transformer ce prototype en application complète
sont décrites dans [PLAN.md](PLAN.md).
Des compléments, dont l'analyse du PDF, les personas et la documentation détaillée de l'API, sont disponibles dans le répertoire [docs](docs).
La liste des tâches en cours figure dans [TODO.md](TODO.md).
