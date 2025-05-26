"""Gestion des cycles d'entraînement.

Ce module esquisse la structure macrocycle -> mesocycles -> microcycles.
Les microcycles représentent les semaines avec progression de la charge
sur quatre semaines suivies d'une semaine allégée.

Ce fichier prépare l'implémentation du point 2 de TODO.md.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List
from .models import TrainingSession


@dataclass
class Microcycle:
    """Une semaine d'entraînement."""
    start: date
    sessions: List[int] = field(default_factory=list)  # ids des séances
    deload: bool = False
    load_factor: float = 1.0


@dataclass
class Mesocycle:
    """Regroupe plusieurs microcycles."""
    start: date
    microcycles: List[Microcycle] = field(default_factory=list)


@dataclass
class Macrocycle:
    """Planification sur l'ensemble de la saison."""
    start: date
    mesocycles: List[Mesocycle] = field(default_factory=list)


def generate_macrocycle(start: date, weeks: int) -> Macrocycle:
    """Crée une structure de macrocycle basique avec montée de charge."""
    macro = Macrocycle(start=start)
    current = start
    factors = [1.0, 1.1, 1.2, 1.3, 0.8]
    for _ in range(0, weeks, 5):
        meso = Mesocycle(start=current)
        for w, factor in enumerate(factors):
            mc = Microcycle(
                start=current + timedelta(weeks=w),
                deload=(w == 4),
                load_factor=factor,
            )
            meso.microcycles.append(mc)
        macro.mesocycles.append(meso)
        current += timedelta(weeks=5)
    return macro


def plan_sessions(
    macro: Macrocycle,
    base: TrainingSession,
    sessions_per_week: int = 3,
) -> List[TrainingSession]:
    """Génère un ensemble de séances à partir d'un macrocycle.

    Chaque microcycle applique son ``load_factor`` pour ajuster la durée de la
    séance de base. Les séances sont espacées de deux jours.
    """

    planned: List[TrainingSession] = []
    sid = 1
    for meso in macro.mesocycles:
        for mc in meso.microcycles:
            for i in range(sessions_per_week):
                session_date = mc.start + timedelta(days=i * 2)
                sess = TrainingSession(
                    id=sid,
                    date=session_date,
                    sport=base.sport,
                    description=base.description,
                    duration_min=int(base.duration_min * mc.load_factor),
                    rpe=base.rpe,
                )
                planned.append(sess)
                mc.sessions.append(sid)
                sid += 1
    return planned
