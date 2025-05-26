# Documentation de l'API

Cette section répertorie les endpoints disponibles dans `packages/api`.

| Méthode | Endpoint | Description |
| ------- | -------- | ----------- |
| `GET`   | `/health` | Vérifie que l'API fonctionne. |
| `GET`   | `/sessions` | Liste toutes les séances enregistrées. |
| `POST`  | `/sessions` | Ajoute une séance. |
| `GET`   | `/sessions/today` | Séances prévues pour aujourd'hui. |
| `GET`   | `/sessions/week` | Séances de la semaine (paramètre `start` optionnel). |
| `PUT`   | `/sessions/{id}` | Met à jour une séance. |
| `GET`   | `/nutrition` | Liste des entrées nutritionnelles. |
| `POST`  | `/nutrition` | Ajoute une entrée nutritionnelle. |
| `GET`   | `/injuries` | Liste des blessures enregistrées. |
| `POST`  | `/injuries` | Ajoute une blessure et ajuste le plan. |
| `PUT`   | `/injuries/{id}` | Met à jour une blessure. |
| `GET`   | `/competitions` | Liste des compétitions. |
| `POST`  | `/competitions` | Ajoute une compétition et ajuste les séances. |
| `POST`  | `/workouts/order` | Réordonne les séances. |
| `POST`  | `/plan/adjust` | Applique le moteur de règles sur les séances futures. |
| `GET`   | `/stats/acwr` | ACWR courant. |
| `GET`   | `/stats/summary` | Charges hebdomadaires et progression. |
| `POST`  | `/nutrition/plan` | Génère un plan nutritionnel. |
| `GET`   | `/cycles` | Génère un macrocycle d'entraînement. |

## Démarrage rapide

```bash
pip install -r packages/api/requirements.txt
cd packages/api
uvicorn app.main:app --reload
```

La documentation interactive est alors accessible sur <http://localhost:8000/docs>.
