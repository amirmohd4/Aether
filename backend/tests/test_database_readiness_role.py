from fastapi.testclient import TestClient

from backend import database
from backend.main import app


class _FakeResult:
    def __init__(self, value):
        self.value = value

    def scalar(self):
        return self.value


class _FakeConnection:
    def __init__(self, role):
        self.role = role

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def exec_driver_sql(self, statement):
        if statement == "SELECT current_user":
            return _FakeResult(self.role)
        return _FakeResult(1)


class _FakeEngine:
    def __init__(self, role):
        self.role = role

    def connect(self):
        return _FakeConnection(self.role)


def test_ready_rejects_superuser_when_runtime_role_is_required(monkeypatch):
    monkeypatch.setenv("AETHER_DATABASE_EXPECTED_ROLE", "aether_runtime")
    monkeypatch.setattr(database, "engine", _FakeEngine("postgres"))

    response = TestClient(app).get("/ready")

    assert response.status_code == 503
    assert response.json()["database"] == "wrong_runtime_role"
    assert response.json()["database_role_valid"] is False


def test_ready_accepts_expected_least_privilege_role(monkeypatch):
    monkeypatch.setenv("AETHER_DATABASE_EXPECTED_ROLE", "aether_runtime")
    monkeypatch.setattr(database, "engine", _FakeEngine("aether_runtime"))

    response = TestClient(app).get("/ready")

    assert response.status_code == 200
    assert response.json()["database"] == "ready"
    assert response.json()["database_role_valid"] is True
