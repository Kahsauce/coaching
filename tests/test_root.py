import os
import sys
import pytest

sys.path.append(os.path.abspath('packages/api'))

main = pytest.importorskip('app.main', reason='fastapi not available')
pytest.importorskip('fastapi')
from app.db import InMemoryDB
from fastapi.testclient import TestClient


def get_client() -> TestClient:
    main.DB = InMemoryDB()
    return TestClient(main.app)


def test_root_redirect():
    client = get_client()
    resp = client.get('/', allow_redirects=False)
    assert resp.status_code in (302, 307)
    assert resp.headers['location'] == '/docs'
