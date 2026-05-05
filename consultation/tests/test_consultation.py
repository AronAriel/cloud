from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_get_consultations(monkeypatch):
    class FakeConsultation:
        def __init__(self):
            self.id = 1
            self.pet_name = "Dog"
            self.date = "2024-01-01"
            self.vet_id = 10

    class FakeDB:
        def query(self, model):
            return self

        def all(self):
            return [FakeConsultation()]

    monkeypatch.setattr("main.SessionLocal", lambda: FakeDB())

    response = client.get("/consultations")

    assert response.status_code == 200
    data = response.json()
    assert data[0]["pet_name"] == "Dog"


def test_create_consultation(monkeypatch):
    class FakeDB:
        def add(self, x): pass
        def commit(self): pass

    monkeypatch.setattr("main.SessionLocal", lambda: FakeDB())
    monkeypatch.setattr("main.send_message", lambda x: None)

    response = client.post("/consultations", json={
        "pet_name": "Cat",
        "date": "2024-01-01",
        "vet_id": 1
    })

    assert response.status_code == 200
    assert response.json()["message"] == "created"