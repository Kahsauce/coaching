from datetime import date, timedelta
from typing import List

from .models import TrainingSession


def compute_acwr(sessions: List[TrainingSession], today: date | None = None) -> float:
    """Compute the acute:chronic workload ratio.

    Acute load = sum of load over last 7 days
    Chronic load = average weekly load over last 28 days
    Load of a session = duration_min * (rpe or 0)
    """
    if today is None:
        today = date.today()
    seven_days_ago = today - timedelta(days=6)
    four_weeks_ago = today - timedelta(days=27)

    acute_load = sum(
        (s.duration_min * (s.rpe or 0))
        for s in sessions
        if seven_days_ago <= s.date <= today
    )

    chronic_load_total = sum(
        (s.duration_min * (s.rpe or 0))
        for s in sessions
        if four_weeks_ago <= s.date <= today
    )
    chronic_load = chronic_load_total / 4  # average per week

    if chronic_load == 0:
        return 0.0
    return acute_load / chronic_load
