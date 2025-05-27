import os
import secrets
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session, select

from src.sport_plan import (
    engine,
    UserProfile,
    SessionModel,
    init_db,
    compute_acute_load,
    compute_chronic_load,
    compute_acwr,
)

security = HTTPBasic()

def require_auth(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    pwd = os.getenv("APP_PASSWORD")
    valid = credentials.username == "admin" and pwd and secrets.compare_digest(credentials.password, pwd)
    if not valid:
        raise HTTPException(status_code=401, detail="Unauthorized")

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    init_db()

@app.post("/profiles")
def create_profile(profile: UserProfile, _: HTTPBasicCredentials = Depends(require_auth)) -> UserProfile:
    with Session(engine) as session:
        session.add(profile)
        session.commit()
        session.refresh(profile)
        return profile

@app.post("/sessions")
def create_session(session_data: SessionModel, _: HTTPBasicCredentials = Depends(require_auth)) -> SessionModel:
    if session_data.duration <= 0:
        raise HTTPException(status_code=400, detail="Durée invalide")
    if not 1 <= session_data.rpe <= 10:
        raise HTTPException(status_code=400, detail="RPE invalide")
    if session_data.date > datetime.today().date():
        raise HTTPException(status_code=400, detail="Date dans le futur interdite")
    with Session(engine) as session:
        session.add(session_data)
        session.commit()
        session.refresh(session_data)
        return session_data

@app.get("/sessions")
def list_all_sessions(_: HTTPBasicCredentials = Depends(require_auth)):
    with Session(engine) as session:
        return session.exec(select(SessionModel)).all()

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


@app.delete("/sessions/{session_id}")
def delete_session(session_id: int, _: HTTPBasicCredentials = Depends(require_auth)) -> dict:
    with Session(engine) as session:
        obj = session.get(SessionModel, session_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Session not found")
        session.delete(obj)
        session.commit()
    return {"status": "deleted"}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def root() -> FileResponse:
    return FileResponse("static/index.html")
