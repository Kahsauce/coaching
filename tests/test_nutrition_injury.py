import os
import sys
from datetime import date, timedelta

sys.path.append(os.path.abspath("packages/api"))

from app.db import InMemoryDB
from app.models import NutritionEntry, Injury, TrainingSession
from app.rule_engine import adjust_sessions


def test_nutrition_entry_added_to_db():
    db = InMemoryDB()
    entry = NutritionEntry(id=0, date=date.today(), calories=2000, hydration_l=2.0)
    stored = db.add_nutrition(entry)
    assert stored.id == 1
    assert db.list_nutrition()[0].calories == 2000


def test_adjust_sessions_with_injury():
    upcoming = TrainingSession(
        id=1,
        date=date.today() + timedelta(days=1),
        sport="run",
        duration_min=60,
        rpe=5,
    )
    injury = Injury(id=0, start_date=date.today(), end_date=date.today() + timedelta(days=2))
    adjusted = adjust_sessions([upcoming], injuries=[injury], today=date.today())
    assert adjusted[0].duration_min == 30
