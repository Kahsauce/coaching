import os
import sys
from datetime import date

sys.path.append(os.path.abspath("packages/api"))

from app.sqlite_db import SQLiteDB
from app.models import TrainingSession, NutritionEntry, Injury, Competition


def make_session() -> TrainingSession:
    return TrainingSession(id=0, date=date.today(), sport="run", duration_min=30)


def test_sqlite_add_and_list():
    db = SQLiteDB(path=":memory:")
    added = db.add_session(make_session())
    assert added.id > 0
    sessions = db.list_sessions()
    assert len(sessions) == 1
    assert sessions[0].id == added.id


def test_sqlite_reorder():
    db = SQLiteDB(path=":memory:")
    s1 = db.add_session(make_session())
    s2 = db.add_session(make_session())
    ordered = db.reorder_sessions([s2.id, s1.id])
    assert [s.id for s in ordered] == [s2.id, s1.id]


def test_sqlite_persist_file(tmp_path):
    path = tmp_path / "test.db"
    db = SQLiteDB(path=str(path))
    db.add_session(make_session())
    db.conn.close()
    new_db = SQLiteDB(path=str(path))
    assert len(new_db.list_sessions()) == 1


def test_sqlite_other_tables():
    db = SQLiteDB(path=":memory:")
    n = db.add_nutrition(
        NutritionEntry(
            id=0,
            date=date.today(),
            calories=2000,
            hydration_l=2.0,
            carbs_g=250,
            protein_g=100,
            fat_g=70,
        )
    )
    assert n.id > 0
    assert len(db.list_nutrition()) == 1
    injury = db.add_injury(Injury(id=0, start_date=date.today()))
    assert injury.id > 0
    assert len(db.list_injuries()) == 1
    comp = db.add_competition(Competition(id=0, date=date.today(), name="10k"))
    assert comp.id > 0
    assert len(db.list_competitions()) == 1
