import os
import pytest
from sqlmodel import create_engine

import server
from src import sport_plan

@pytest.fixture
def engine(tmp_path):
    db = tmp_path / "test.db"
    url = f"sqlite:///{db}"
    os.environ["DATABASE_URL"] = url
    sport_plan.engine = create_engine(url, echo=False)
    server.engine = sport_plan.engine
    sport_plan.init_db()
    return sport_plan.engine
