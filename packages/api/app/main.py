from fastapi import FastAPI, HTTPException
from typing import List, Optional
from datetime import date, timedelta

from .acwr import compute_acwr
from .rule_engine import adjust_sessions
from .stats import stats_summary
from .nutrition import calculate_plan, NutritionPlanRequest
from .cycles import generate_macrocycle, Macrocycle

from .models import TrainingSession, NutritionEntry, Injury, Competition
from .database import DB

app = FastAPI(title="Coaching App")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/sessions", response_model=List[TrainingSession])
def list_sessions():
    return DB.list_sessions()

@app.post("/sessions", response_model=TrainingSession)
def create_session(session: TrainingSession):
    return DB.add_session(session)

@app.get("/sessions/today", response_model=List[TrainingSession])
def sessions_today():
    today = date.today()
    return [s for s in DB.list_sessions() if s.date == today]


@app.get("/sessions/week", response_model=List[TrainingSession])
def sessions_week(start: Optional[date] = None):
    start_date = start or date.today()
    monday = start_date - timedelta(days=start_date.weekday())
    return DB.sessions_for_week(monday)

@app.put("/sessions/{session_id}", response_model=TrainingSession)
def update_session(session_id: int, session: TrainingSession):
    if not DB.get_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    session.id = session_id
    return DB.update_session(session_id, session)


@app.get("/nutrition", response_model=List[NutritionEntry])
def list_nutrition():
    return DB.list_nutrition()


@app.post("/nutrition", response_model=NutritionEntry)
def add_nutrition(entry: NutritionEntry):
    return DB.add_nutrition(entry)


@app.get("/injuries", response_model=List[Injury])
def list_injuries():
    return DB.list_injuries()


@app.post("/injuries", response_model=Injury)
def add_injury(injury: Injury):
    stored = DB.add_injury(injury)
    # Mise à jour immédiate du plan d'entraînement
    sessions = DB.list_sessions()
    injuries = DB.list_injuries()
    competitions = DB.list_competitions()
    adjusted = adjust_sessions(sessions, injuries=injuries, competitions=competitions)
    for s in adjusted:
        DB.update_session(s.id, s)
    return stored


@app.put("/injuries/{injury_id}", response_model=Injury)
def update_injury(injury_id: int, injury: Injury):
    if not any(i.id == injury_id for i in DB.list_injuries()):
        raise HTTPException(status_code=404, detail="Injury not found")
    updated = DB.update_injury(injury_id, injury)
    # Recalculate plan after injury update
    sessions = DB.list_sessions()
    injuries = DB.list_injuries()
    competitions = DB.list_competitions()
    adjusted = adjust_sessions(sessions, injuries=injuries, competitions=competitions)
    for s in adjusted:
        DB.update_session(s.id, s)
    return updated


@app.get("/competitions", response_model=List[Competition])
def list_competitions():
    return DB.list_competitions()


@app.post("/competitions", response_model=Competition)
def add_competition(comp: Competition):
    return DB.add_competition(comp)


@app.post("/workouts/order", response_model=List[TrainingSession])
def reorder_sessions(order: List[int]):
    """Reorder sessions according to given list of ids."""
    return DB.reorder_sessions(order)


@app.post("/plan/adjust", response_model=List[TrainingSession])
def plan_adjust():
    """Apply rule engine to adapt upcoming sessions."""
    sessions = DB.list_sessions()
    injuries = DB.list_injuries()
    competitions = DB.list_competitions()
    adjusted = adjust_sessions(sessions, injuries=injuries, competitions=competitions)
    # sessions are modified in place, update DB entries
    for s in adjusted:
        DB.update_session(s.id, s)
    return adjusted


@app.get("/stats/acwr")
def get_acwr():
    """Return the current ACWR metric."""
    ratio = compute_acwr(DB.list_sessions())
    return {"acwr": ratio}


@app.get("/stats/summary")
def get_stats_summary():
    """Return ACWR, weekly loads and progression."""
    sessions = DB.list_sessions()
    return stats_summary(sessions)


@app.post("/nutrition/plan")
def get_nutrition_plan(req: NutritionPlanRequest):
    """Return a basic nutrition plan from body weight and goal."""
    return calculate_plan(req.body_weight_kg, req.goal)


@app.get("/cycles", response_model=Macrocycle)
def create_macrocycle(start: date, weeks: int = 20):
    """Generate a basic macrocycle starting at given date."""
    return generate_macrocycle(start, weeks)
