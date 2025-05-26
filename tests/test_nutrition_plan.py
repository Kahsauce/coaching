import os
import sys
from datetime import date

sys.path.append(os.path.abspath("packages/api"))

from app.nutrition import calculate_plan


def test_calculate_plan_fields():
    plan = calculate_plan(70, "maintain")
    assert plan.calories > 0
    assert plan.protein_g > 0
    assert plan.carbs_g > 0
    assert plan.fat_g > 0
    assert plan.hydration_l > 0
