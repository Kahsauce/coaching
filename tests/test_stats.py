import os
import sys
from datetime import date, timedelta

sys.path.append(os.path.abspath("packages/api"))

from app.stats import weekly_loads, progression, stats_summary
from app.models import TrainingSession


def make_session(days_ago: int, duration: int, rpe: int) -> TrainingSession:
    return TrainingSession(
        id=0,
        date=date.today() - timedelta(days=days_ago),
        sport="run",
        duration_min=duration,
        rpe=rpe,
    )


def test_weekly_loads_and_progression():
    sessions = [
        make_session(1, 60, 5),
        make_session(8, 60, 5),
        make_session(15, 60, 5),
        make_session(22, 60, 5),
    ]
    loads = weekly_loads(sessions, today=date.today())
    assert len(loads) == 4
    prog = progression(sessions, today=date.today())
    assert isinstance(prog, float)


def test_stats_summary_returns_keys():
    sessions = [make_session(1, 60, 5)]
    summary = stats_summary(sessions, today=date.today())
    assert "acwr" in summary
    assert "weekly_loads" in summary
    assert "progression" in summary
