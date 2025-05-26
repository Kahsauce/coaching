import os
import sys
from datetime import date, timedelta

sys.path.append(os.path.abspath("packages/api"))

from app.nutrition import calculate_plan, average_hydration
from app.models import NutritionEntry


def test_calculate_plan_fields():
    plan = calculate_plan(70, "maintain")
    assert plan.calories > 0
    assert plan.protein_g > 0
    assert plan.carbs_g > 0
    assert plan.fat_g > 0
    assert plan.hydration_l > 0


def test_average_hydration():
    entries = [
        NutritionEntry(id=i, date=date.today() - timedelta(days=i), calories=2000, hydration_l=2.0, carbs_g=200, protein_g=100, fat_g=70)
        for i in range(3)
    ]
    avg = average_hydration(entries, days=2, today=date.today())
    assert 1.9 < avg < 2.1
