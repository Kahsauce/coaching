import os
from fastapi.testclient import TestClient

import server
from src import sport_plan

TEST_DB = "api_test.db"


def setup_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
    sport_plan.engine = sport_plan.create_engine(os.environ["DATABASE_URL"], echo=False)
    server.engine = sport_plan.engine
    sport_plan.init_db()


def teardown_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

client = TestClient(server.app)


def test_create_and_metrics():
    r = client.post("/profiles", json={"name": "Bob", "age": 25, "weight": 70, "height": 175, "sports": "['course']"})
    assert r.status_code == 200
    r = client.post("/sessions", json={"date": "2023-01-01", "activity_type": "course", "duration": 30, "rpe": 5})
    assert r.status_code == 200
    r = client.get("/metrics?date=2023-01-01")
    assert r.status_code == 200
    data = r.json()
    assert "acwr" in data
