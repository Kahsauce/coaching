# Coaching App

Cette application propose une petite API et une page HTML pour gérer vos séances sportives et calculer l'ACWR.

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Version recommandée : **Python 3.12**

## Lancement du serveur

```
make dev
```
Ou bien :
```
npm run dev
```

La page `index.html` est servie directement par l'API FastAPI.

## Variables d'environnement

- `DATABASE_URL` : URL de la base (par défaut `sqlite:///app.db`).
- `APP_PASSWORD` : mot de passe pour les routes protégées `/profiles` et `/sessions`.

## Tests

```
make test
```
