import os
import base64
import httpx
import pytest
from fastapi.testclient import TestClient

import server
from src import sport_plan


@pytest.fixture
def client(tmp_path):
    db = tmp_path / "api.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db}"
    os.environ["APP_PASSWORD"] = "testpwd"
    sport_plan.engine = sport_plan.create_engine(os.environ["DATABASE_URL"], echo=False)
    server.engine = sport_plan.engine
    sport_plan.init_db()
    with TestClient(server.app) as c:
        yield c


def test_create_and_metrics(client):
    headers = {"Authorization": "Basic " + base64.b64encode(b"admin:testpwd").decode()}
    r = client.post("/profiles", json={"name": "Bob", "age": 25, "weight": 70, "height": 175, "sports": "['course']"}, headers=headers)
    assert r.status_code == 200
    r = client.post("/sessions", json={"date": "2023-01-01", "activity_type": "course", "duration": 30, "rpe": 5}, headers=headers)
    assert r.status_code == 200
    r = client.get("/metrics?date=2023-01-01", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert "acwr" in data


@pytest.mark.asyncio
async def test_e2e(tmp_path):
    os.environ["DATABASE_URL"] = f"sqlite:///{tmp_path/'e2e.db'}"
    os.environ["APP_PASSWORD"] = "pwd"
    sport_plan.engine = sport_plan.create_engine(os.environ["DATABASE_URL"], echo=False)
    server.engine = sport_plan.engine
    sport_plan.init_db()
    async with httpx.AsyncClient(app=server.app, base_url="http://test") as ac:
        auth = ("admin", "pwd")
        r = await ac.post("/sessions", json={"date": "2023-01-02", "activity_type": "course", "duration": 20, "rpe": 5}, auth=auth)
        assert r.status_code == 200
        r = await ac.get("/sessions", auth=auth)
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 1
