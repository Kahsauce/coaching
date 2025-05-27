from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from datetime import datetime

from src.sport_plan import (
    engine,
    UserProfile,
    SessionModel,
    init_db,
    compute_acute_load,
    compute_chronic_load,
    compute_acwr,
)

app = FastAPI()
app.mount("/", StaticFiles(directory=".", html=True), name="static")

@app.on_event("startup")
def on_startup() -> None:
    init_db()

@app.post("/profiles")
def create_profile(profile: UserProfile) -> UserProfile:
    with Session(engine) as session:
        session.add(profile)
        session.commit()
        session.refresh(profile)
        return profile

@app.post("/sessions")
def create_session(session_data: SessionModel) -> SessionModel:
    with Session(engine) as session:
        session.add(session_data)
        session.commit()
        session.refresh(session_data)
        return session_data

@app.get("/metrics")
def get_metrics(date: str) -> dict:
    try:
        today = datetime.fromisoformat(date).date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    with Session(engine) as session:
        sessions = session.exec(select(SessionModel)).all()
    acute = compute_acute_load(sessions, today)
    chronic = compute_chronic_load(sessions, today)
    acwr = compute_acwr(sessions, today)
    return {"acute": acute, "chronic": chronic, "acwr": acwr}
