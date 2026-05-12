from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_graphql_vets_query(monkeypatch):
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

    response = client.post(
        "/graphql",
        json={
            "query": """
                query {
                    vets {
                        id
                        name
                        specialization
                    }
                }
            """
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["data"]["vets"] == [
        {
            "id": 1,
            "name": "Dr. Smith",
            "specialization": "Surgery",
        }
    ]
