from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_get_feedbacks(monkeypatch):
    class FakeFeedback:
        def __init__(self):
            self.id = 1
            self.consultation_id = 2
            self.rating = 5
            self.comment = "Great"

    class FakeDB:
        def query(self, model):
            return self

        def all(self):
            return [FakeFeedback()]

    monkeypatch.setattr("main.SessionLocal", lambda: FakeDB())

    response = client.get("/feedbacks")

    assert response.status_code == 200
    data = response.json()

    assert data[0]["rating"] == 5