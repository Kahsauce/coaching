import os
import sys
from datetime import date

sys.path.append(os.path.abspath("packages/api"))

from app.cycles import generate_macrocycle


def test_macrocycle_load_factors():
    macro = generate_macrocycle(date(2025, 1, 1), weeks=5)
    factors = [mc.load_factor for mc in macro.mesocycles[0].microcycles]
    assert factors == [1.0, 1.1, 1.2, 1.3, 0.8]
