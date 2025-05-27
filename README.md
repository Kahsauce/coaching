# Coaching App

Cette application propose une petite API et une page HTML pour gérer vos séances sportives et calculer l'ACWR.

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Lancement du serveur

```
make dev
```
Ou bien :
```
npm run dev
```

La page `index.html` est servie directement par l'API FastAPI.

## Tests

```
make test
```
