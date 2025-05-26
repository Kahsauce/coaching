import os
import sys
from datetime import date, timedelta

sys.path.append(os.path.abspath("packages/api"))

from app.rule_engine import adjust_sessions
from app.models import TrainingSession


def make_session(days_ahead: int, duration: int, rpe: int = 5) -> TrainingSession:
    session_date = date.today() + timedelta(days=days_ahead)
    return TrainingSession(id=0, date=session_date, sport="run", duration_min=duration, rpe=rpe)


def test_adjust_sessions_reduces_load_when_acwr_high():
    past = TrainingSession(id=1, date=date.today() - timedelta(days=1), sport="run", duration_min=120, rpe=10)
    upcoming = make_session(1, 60)
    sessions = [past, upcoming]
    adjusted = adjust_sessions(sessions, today=date.today())
    assert adjusted[1].duration_min < 60
