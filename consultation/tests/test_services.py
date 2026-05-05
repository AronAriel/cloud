from services import (
    create_consultation,
    list_consultations,
    send_service_bus_message,
    serialize_consultation,
)


class FakeConsultation:
    id = 7
    pet_name = "Cat"
    date = "2024-01-01"
    vet_id = 3


class FakePayload:
    pet_name = "Cat"
    date = "2024-01-01"
    vet_id = 3


def test_serialize_consultation_returns_api_contract():
    assert serialize_consultation(FakeConsultation()) == {
        "id": 7,
        "pet_name": "Cat",
        "date": "2024-01-01",
        "vet_id": 3,
    }


def test_list_consultations_queries_and_serializes_items():
    class FakeQuery:
        def all(self):
            return [FakeConsultation()]

    class FakeDB:
        def query(self, model):
            self.model = model
            return FakeQuery()

    assert list_consultations(FakeDB()) == [
        {
            "id": 7,
            "pet_name": "Cat",
            "date": "2024-01-01",
            "vet_id": 3,
        }
    ]


def test_create_consultation_persists_and_sends_message():
    sent_messages = []

    class FakeDB:
        def add(self, item):
            item.id = 12
            self.added_item = item

        def commit(self):
            self.committed = True

    db = FakeDB()

    result = create_consultation(db, FakePayload(), sent_messages.append)

    assert result == {"message": "created"}
    assert db.added_item.pet_name == "Cat"
    assert db.committed is True
    assert sent_messages == ["New consultation created: 12"]


def test_send_service_bus_message_uses_configured_queue(monkeypatch):
    calls = []

    class FakeSender:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def send_messages(self, message):
            calls.append(("send", str(message)))

    class FakeClient:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get_queue_sender(self, queue_name):
            calls.append(("queue", queue_name))
            return FakeSender()

    class FakeServiceBusClient:
        @staticmethod
        def from_connection_string(connection_string):
            calls.append(("connection", connection_string))
            return FakeClient()

    monkeypatch.setattr("services.ServiceBusClient", FakeServiceBusClient)
    monkeypatch.setattr("services.ServiceBusMessage", lambda message: message)

    send_service_bus_message("Endpoint=sb://example", "consultations", "Created")

    assert calls == [
        ("connection", "Endpoint=sb://example"),
        ("queue", "consultations"),
        ("send", "Created"),
    ]
