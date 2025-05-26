from datetime import date, timedelta

import os
import sys

sys.path.append(os.path.abspath("backend"))

from app.acwr import compute_acwr
from app.models import TrainingSession


def make_session(days_ago: int, duration: int, rpe: int) -> TrainingSession:
    session_date = date.today() - timedelta(days=days_ago)
    return TrainingSession(id=0, date=session_date, sport="run", duration_min=duration, rpe=rpe)


def test_acwr_basic():
    sessions = [
        make_session(1, 60, 5),
        make_session(3, 30, 5),
        make_session(8, 60, 5),
        make_session(15, 60, 5),
        make_session(22, 60, 5),
    ]
    ratio = compute_acwr(sessions, today=date.today())
    assert ratio > 0
