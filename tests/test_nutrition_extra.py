import os
import sys
from datetime import date, timedelta

sys.path.append(os.path.abspath('packages/api'))

from app.nutrition import average_hydration
from app.models import NutritionEntry


def test_average_hydration_no_entries():
    assert average_hydration([], days=3, today=date.today()) == 0.0


def test_average_hydration_out_of_range():
    entries = [
        NutritionEntry(id=1, date=date.today() - timedelta(days=10), calories=2000, hydration_l=2.0, carbs_g=200, protein_g=100, fat_g=70)
    ]
    assert average_hydration(entries, days=3, today=date.today()) == 0.0
