import os
import sys
from datetime import date

sys.path.append(os.path.abspath("packages/api"))

from app.sqlite_db import SQLiteDB
from app.models import TrainingSession


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
