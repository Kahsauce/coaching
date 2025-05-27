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
Ou directement :
```
uvicorn server:app --reload --workers 1
```

La page `index.html` est servie directement par l'API FastAPI.

## Variables d'environnement

- `DATABASE_URL` : URL de la base (par défaut `sqlite:///app.db`).
- `APP_PASSWORD` : mot de passe pour les routes protégées `/profiles` et `/sessions`.

L'interface Web demande ce mot de passe via un prompt JavaScript avant les appels API protégés.

Pour la production, stockez votre fichier `.env` hors du dépôt et instanciez `FastAPI(docs_url=None)` pour désactiver la documentation interactive.

## Tests

```
make test
```
