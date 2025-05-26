from datetime import date
from typing import List

from .models import TrainingSession
from .acwr import compute_acwr


def adjust_sessions(sessions: List[TrainingSession], today: date | None = None) -> List[TrainingSession]:
    """Simple rule engine adjusting future sessions based on ACWR.

    If the current ACWR is above 1.5, future sessions duration is reduced by 20%.
    """
    ratio = compute_acwr(sessions, today=today)
    if today is None:
        today = date.today()

    if ratio > 1.5:
        for s in sessions:
            if not s.completed and s.date >= today:
                s.duration_min = int(s.duration_min * 0.8)
    return sessions
