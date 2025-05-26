import os
import sys
from datetime import date, timedelta

sys.path.append(os.path.abspath("packages/api"))

from app.db import InMemoryDB
from app.models import TrainingSession, Competition
from app.rule_engine import adjust_sessions


def test_add_competition_to_db():
    db = InMemoryDB()
    comp = Competition(id=0, date=date.today(), name="10k")
    stored = db.add_competition(comp)
    assert stored.id == 1
    assert db.list_competitions()[0].name == "10k"


def test_adjust_sessions_with_competition():
    comp_date = date.today() + timedelta(days=2)
    session = TrainingSession(id=1, date=comp_date - timedelta(days=1), sport="run", duration_min=60)
    adjusted = adjust_sessions([session], competitions=[Competition(id=1, date=comp_date, name="10k")], today=date.today())
    assert adjusted[0].duration_min == 33
