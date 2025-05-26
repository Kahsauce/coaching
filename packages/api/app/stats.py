from datetime import date, timedelta
from typing import List

from .models import TrainingSession
from .acwr import compute_acwr


def weekly_loads(sessions: List[TrainingSession], today: date | None = None) -> List[int]:
    """Return total load for each of the last 4 weeks (current week included)."""
    if today is None:
        today = date.today()
    # Monday of current week
    monday = today - timedelta(days=today.weekday())
    loads = []
    for i in range(4):
        start = monday - timedelta(days=i * 7)
        end = start + timedelta(days=6)
        total = sum(
            (s.duration_min * (s.rpe or 0))
            for s in sessions
            if start <= s.date <= end
        )
        loads.append(total)
    return list(reversed(loads))


def progression(sessions: List[TrainingSession], today: date | None = None) -> float:
    """Simple progression metric: percentage change between last week and first of last 4 weeks."""
    loads = weekly_loads(sessions, today=today)
    if not loads or loads[0] == 0:
        return 0.0
    return (loads[-1] - loads[0]) / loads[0] * 100


def stats_summary(sessions: List[TrainingSession], today: date | None = None) -> dict:
    """Return ACWR plus weekly loads and progression."""
    if today is None:
        today = date.today()
    return {
        "acwr": compute_acwr(sessions, today=today),
        "weekly_loads": weekly_loads(sessions, today=today),
        "progression": progression(sessions, today=today),
    }
