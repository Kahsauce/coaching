import base64
import httpx
import os
import pytest
from fastapi.testclient import TestClient

import server
from src import sport_plan


@pytest.fixture
def client(engine):
    os.environ["APP_PASSWORD"] = "testpwd"
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


def test_delete_session(client):
    headers = {"Authorization": "Basic " + base64.b64encode(b"admin:testpwd").decode()}
    r = client.post("/sessions", json={"date": "2023-01-03", "activity_type": "course", "duration": 40, "rpe": 6}, headers=headers)
    assert r.status_code == 200
    sid = r.json()["id"]
    r = client.delete(f"/sessions/{sid}", headers=headers)
    assert r.status_code == 200
    r = client.get("/sessions", headers=headers)
    assert r.json() == []


def test_invalid_activity(client):
    headers = {"Authorization": "Basic " + base64.b64encode(b"admin:testpwd").decode()}
    r = client.post("/sessions", json={"date": "2023-01-01", "activity_type": "unknown", "duration": 30, "rpe": 5}, headers=headers)
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_e2e(engine):
    os.environ["APP_PASSWORD"] = "pwd"
    async with httpx.AsyncClient(app=server.app, base_url="http://test") as ac:
        auth = ("admin", "pwd")
        r = await ac.post("/sessions", json={"date": "2023-01-02", "activity_type": "course", "duration": 20, "rpe": 5}, auth=auth)
        assert r.status_code == 200
        r = await ac.get("/sessions", auth=auth)
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 1
        sid = data[0]["id"]
        r = await ac.delete(f"/sessions/{sid}", auth=auth)
        assert r.status_code == 200
        r = await ac.get("/sessions", auth=auth)
        assert r.json() == []
