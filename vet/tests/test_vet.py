from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_get_vets(monkeypatch):
    class FakeVet:
        def __init__(self):
            self.id = 1
            self.name = "Dr. Smith"
            self.specialization = "Surgery"

    class FakeDB:
        def query(self, model):
            return self

        def all(self):
            return [FakeVet()]

    monkeypatch.setattr("main.SessionLocal", lambda: FakeDB())

    response = client.get("/vets")

    assert response.status_code == 200
    data = response.json()

    assert data[0]["name"] == "Dr. Smith"