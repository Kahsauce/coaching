from datetime import date
import os
import sys

sys.path.append(os.path.abspath("packages/api"))

from app.db import InMemoryDB
from app.models import TrainingSession


def make_session(id: int) -> TrainingSession:
    return TrainingSession(id=id, date=date.today(), sport="run", duration_min=30)


def test_reorder_sessions():
    db = InMemoryDB()
    s1 = db.add_session(make_session(0))
    s2 = db.add_session(make_session(0))
    s3 = db.add_session(make_session(0))

    ordered = db.reorder_sessions([s3.id, s1.id, s2.id])
    assert [s.id for s in ordered] == [s3.id, s1.id, s2.id]
