import os
import sys
from datetime import date, timedelta

sys.path.append(os.path.abspath("packages/api"))

from app.db import InMemoryDB
from app.models import NutritionEntry, Injury, TrainingSession
from app.rule_engine import adjust_sessions


def test_nutrition_entry_added_to_db():
    db = InMemoryDB()
    entry = NutritionEntry(id=0, date=date.today(), calories=2000, hydration_l=2.0, carbs_g=250, protein_g=120, fat_g=70)
    stored = db.add_nutrition(entry)
    assert stored.id == 1
    saved = db.list_nutrition()[0]
    assert saved.calories == 2000
    assert saved.carbs_g == 250


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
    assert adjusted[0].duration_min == 0
    assert "RICE" in adjusted[0].description


def test_progressive_return_after_injury():
    past_sessions = [
        TrainingSession(id=i, date=date.today() - timedelta(days=d), sport="run", duration_min=60, rpe=5)
        for i, d in enumerate([3, 10, 17, 24], start=1)
    ]
    upcoming = TrainingSession(id=5, date=date.today() + timedelta(days=1), sport="run", duration_min=60, rpe=5)
    injury = Injury(id=0, start_date=date.today() - timedelta(days=3), end_date=date.today() - timedelta(days=1))
    adjusted = adjust_sessions(past_sessions + [upcoming], injuries=[injury], today=date.today())
    returned = adjusted[-1]
    assert returned.duration_min == 45


def test_update_injury_in_memory_db():
    db = InMemoryDB()
    injury = db.add_injury(Injury(id=0, start_date=date.today()))
    injury.end_date = date.today()
    updated = db.update_injury(injury.id, injury)
    assert updated.end_date == date.today()
