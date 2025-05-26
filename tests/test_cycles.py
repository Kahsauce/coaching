import os
import sys
from datetime import date

sys.path.append(os.path.abspath("packages/api"))

from app.cycles import generate_macrocycle, plan_sessions
from app.models import TrainingSession


def test_macrocycle_load_factors():
    macro = generate_macrocycle(date(2025, 1, 1), weeks=5)
    factors = [mc.load_factor for mc in macro.mesocycles[0].microcycles]
    assert factors == [1.0, 1.1, 1.2, 1.3, 0.8]


def test_plan_sessions_uses_load_factor():
    macro = generate_macrocycle(date(2025, 1, 1), weeks=5)
    template = TrainingSession(id=0, date=date(2025, 1, 1), sport="run", duration_min=60, rpe=5)
    sessions = plan_sessions(macro, template, sessions_per_week=1)
    durations = [s.duration_min for s in sessions[:5]]
    assert durations == [60, 66, 72, 78, 48]
