import os
import sys
from datetime import date
import pytest

sys.path.append(os.path.abspath('packages/api'))

main = pytest.importorskip("app.main", reason="fastapi not available")
pytest.importorskip("fastapi")
from app.db import InMemoryDB
from fastapi.testclient import TestClient


def get_client() -> TestClient:
    main.DB = InMemoryDB()
    return TestClient(main.app)


def test_health_endpoint():
    client = get_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json() == {'status': 'ok'}


def test_create_and_list_sessions():
    client = get_client()
    data = {
        'id': 0,
        'date': date.today().isoformat(),
        'sport': 'run',
        'duration_min': 45,
        'rpe': 5
    }
    resp = client.post('/sessions', json=data)
    assert resp.status_code == 200
    session = resp.json()
    resp_list = client.get('/sessions')
    assert resp_list.status_code == 200
    assert len(resp_list.json()) == 1
    assert resp_list.json()[0]['id'] == session['id']
