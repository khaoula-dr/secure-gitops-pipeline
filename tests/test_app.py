import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app  # noqa: E402


def client():
    app.testing = True
    return app.test_client()


def test_root():
    resp = client().get("/")
    assert resp.status_code == 200
    assert "app" in resp.get_json()


def test_health():
    resp = client().get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_ready():
    resp = client().get("/ready")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ready"


def test_info():
    resp = client().get("/info")
    assert resp.status_code == 200
    body = resp.get_json()
    assert "version" in body
    assert "timestamp" in body
