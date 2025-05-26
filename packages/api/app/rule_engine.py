from datetime import date
from typing import List

from .models import TrainingSession, Injury
from .acwr import compute_acwr


def adjust_sessions(
    sessions: List[TrainingSession],
    today: date | None = None,
    injuries: List[Injury] | None = None,
) -> List[TrainingSession]:
    """Ajuste les séances en fonction de l'ACWR et des blessures."""

    ratio = compute_acwr(sessions, today=today)
    if today is None:
        today = date.today()

    if ratio > 1.5:
        for s in sessions:
            if not s.completed and s.date >= today:
                s.duration_min = int(s.duration_min * 0.8)

    if injuries:
        for injury in injuries:
            end = injury.end_date or date.max
            for s in sessions:
                if injury.start_date <= s.date <= end and not s.completed:
                    s.duration_min = int(s.duration_min * 0.5)

    return sessions
