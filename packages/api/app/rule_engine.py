from datetime import date, timedelta
from typing import List

from .models import TrainingSession, Injury, Competition
from .acwr import compute_acwr


def adjust_sessions(
    sessions: List[TrainingSession],
    today: date | None = None,
    injuries: List[Injury] | None = None,
    competitions: List[Competition] | None = None,
) -> List[TrainingSession]:
    """Ajuste les séances en fonction de l'ACWR et des blessures."""

    ratio = compute_acwr(sessions, today=today)
    if today is None:
        today = date.today()

    if ratio > 1.5:
        # Réduire la charge et l'intensité pour limiter le risque de blessure
        for s in sessions:
            if not s.completed and s.date >= today:
                s.duration_min = int(s.duration_min * 0.8)
                if s.rpe is not None:
                    s.rpe = max(1, s.rpe - 2)
    elif ratio < 0.5:
        # Ratio très bas : augmenter franchement la charge et l'intensité
        for s in sessions:
            if not s.completed and s.date >= today:
                s.duration_min = int(s.duration_min * 1.2)
                if s.rpe is not None:
                    s.rpe = min(10, s.rpe + 1)
    elif ratio < 0.8:
        # Augmenter légèrement la charge pour éviter un sous-entraînement
        for s in sessions:
            if not s.completed and s.date >= today:
                s.duration_min = int(s.duration_min * 1.1)
                if s.rpe is not None:
                    s.rpe = min(10, s.rpe + 1)

    if injuries:
        for injury in injuries:
            end = injury.end_date or date.max
            for s in sessions:
                if injury.start_date <= s.date <= end and not s.completed:
                    days_since_start = (s.date - injury.start_date).days
                    if days_since_start < 3:
                        s.description = "Repos - RICE"
                        s.duration_min = 0
                    else:
                        s.duration_min = int(s.duration_min * 0.5)
                # reprise progressive apres la blessure
                if injury.end_date and s.date > injury.end_date and not s.completed:
                    days_after = (s.date - injury.end_date).days
                    if days_after <= 6:
                        s.duration_min = int(s.duration_min * 0.75)
                    elif days_after <= 13:
                        s.duration_min = int(s.duration_min * 0.9)

    if competitions:
        for comp in competitions:
            for s in sessions:
                if comp.date - timedelta(days=3) <= s.date <= comp.date + timedelta(days=1):
                    if s.date == comp.date:
                        s.description = f"Repos - {comp.name}"
                        s.duration_min = 0
                    else:
                        s.duration_min = int(s.duration_min * 0.5)

    return sessions
