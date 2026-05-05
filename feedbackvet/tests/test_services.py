from services import consume_service_bus_messages, list_feedbacks, serialize_feedback


class FakeFeedback:
    id = 4
    consultation_id = 2
    rating = 5
    comment = "Great"


def test_serialize_feedback_returns_api_contract():
    assert serialize_feedback(FakeFeedback()) == {
        "id": 4,
        "consultation_id": 2,
        "rating": 5,
        "comment": "Great",
    }


def test_list_feedbacks_queries_and_serializes_items():
    class FakeQuery:
        def all(self):
            return [FakeFeedback()]

    class FakeDB:
        def query(self, model):
            self.model = model
            return FakeQuery()

    assert list_feedbacks(FakeDB()) == [
        {
            "id": 4,
            "consultation_id": 2,
            "rating": 5,
            "comment": "Great",
        }
    ]


def test_consume_service_bus_messages_completes_each_message():
    class FakeReceiver:
        def __init__(self):
            self.completed = []

        def receive_messages(self, max_message_count):
            self.max_message_count = max_message_count
            return ["one", "two"]

        def complete_message(self, message):
            self.completed.append(message)

    class FakeLogger:
        def info(self, message):
            pass

    receiver = FakeReceiver()

    count = consume_service_bus_messages(receiver, FakeLogger())

    assert count == 2
    assert receiver.max_message_count == 10
    assert receiver.completed == ["one", "two"]
