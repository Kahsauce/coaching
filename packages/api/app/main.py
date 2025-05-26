from fastapi import FastAPI, HTTPException
from typing import List
from datetime import date

from .acwr import compute_acwr
from .rule_engine import adjust_sessions

from .models import TrainingSession
from .db import DB

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

@app.put("/sessions/{session_id}", response_model=TrainingSession)
def update_session(session_id: int, session: TrainingSession):
    if not DB.get_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    session.id = session_id
    return DB.update_session(session_id, session)


@app.post("/workouts/order", response_model=List[TrainingSession])
def reorder_sessions(order: List[int]):
    """Reorder sessions according to given list of ids."""
    return DB.reorder_sessions(order)


@app.post("/plan/adjust", response_model=List[TrainingSession])
def plan_adjust():
    """Apply rule engine to adapt upcoming sessions."""
    sessions = DB.list_sessions()
    adjusted = adjust_sessions(sessions)
    # sessions are modified in place, update DB entries
    for s in adjusted:
        DB.update_session(s.id, s)
    return adjusted


@app.get("/stats/acwr")
def get_acwr():
    """Return the current ACWR metric."""
    ratio = compute_acwr(DB.list_sessions())
    return {"acwr": ratio}
