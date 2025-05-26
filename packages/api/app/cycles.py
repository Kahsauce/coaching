"""Gestion des cycles d'entraînement.

Ce module esquisse la structure macrocycle -> mesocycles -> microcycles.
Les microcycles représentent les semaines avec progression de la charge
sur quatre semaines suivies d'une semaine allégée.

Ce fichier prépare l'implémentation du point 2 de TODO.md.
"""

from pydantic.dataclasses import dataclass
from dataclasses import field
from datetime import date, timedelta
from typing import List


@dataclass
class Microcycle:
    """Une semaine d'entraînement."""
    start: date
    sessions: List[int] = field(default_factory=list)  # ids des séances
    deload: bool = False


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
    for _ in range(0, weeks, 5):
        meso = Mesocycle(start=current)
        for w in range(4):
            mc = Microcycle(start=current + timedelta(weeks=w))
            meso.microcycles.append(mc)
        deload = Microcycle(start=current + timedelta(weeks=4), deload=True)
        meso.microcycles.append(deload)
        macro.mesocycles.append(meso)
        current += timedelta(weeks=5)
    return macro
