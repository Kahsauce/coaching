from datetime import date, datetime, timedelta
from typing import List, Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
engine = create_engine(DATABASE_URL, echo=False)

class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    weight: float
    height: float
    sports: str

class SessionModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    activity_type: str
    duration: int
    rpe: int

    @property
    def srpe(self) -> int:
        return self.duration * self.rpe

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def add_profile(profile: UserProfile) -> None:
    with Session(engine) as session:
        session.add(profile)
        session.commit()

def add_session(session_data: SessionModel) -> None:
    with Session(engine) as session:
        session.add(session_data)
        session.commit()

def list_sessions() -> List[SessionModel]:
    with Session(engine) as session:
        return session.exec(select(SessionModel)).all()

def compute_acute_load(sessions: List[SessionModel], today: date) -> int:
    start = today - timedelta(days=6)
    return sum(s.srpe for s in sessions if start <= s.date <= today)

def compute_chronic_load(sessions: List[SessionModel], today: date) -> float:
    start = today - timedelta(days=27)
    loads = [s.srpe for s in sessions if start <= s.date <= today]
    if not loads:
        return 0.0
    return sum(loads) / 4

def compute_acwr(sessions: List[SessionModel], today: date) -> float:
    chronic = compute_chronic_load(sessions, today)
    if chronic == 0:
        return 0.0
    acute = compute_acute_load(sessions, today)
    return acute / chronic
