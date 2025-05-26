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
    assert adjusted[1].rpe < 5


def test_adjust_sessions_increases_load_when_acwr_low():
    """Si le ratio ACWR est trop bas, la durée doit augmenter."""
    past = TrainingSession(id=1, date=date.today() - timedelta(days=28), sport="run", duration_min=30, rpe=5)
    upcoming = make_session(1, 60)
    sessions = [past, upcoming]
    adjusted = adjust_sessions(sessions, today=date.today())
    assert adjusted[1].duration_min > 60
    assert adjusted[1].rpe > 5


def test_adjust_sessions_boost_when_acwr_very_low():
    past = TrainingSession(id=1, date=date.today() - timedelta(days=28), sport="run", duration_min=30, rpe=5)
    upcoming = make_session(1, 60)
    sessions = [past, upcoming]
    # ratio will be very low (<0.5) since only one low session in chronic period
    adjusted = adjust_sessions(sessions, today=date.today())
    assert adjusted[1].duration_min > 66  # 60 * 1.1 would be 66, expect more
    assert adjusted[1].rpe >= 6
