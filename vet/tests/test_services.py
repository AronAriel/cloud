from services import list_vets, serialize_vet


class FakeVet:
    id = 1
    name = "Dr. Smith"
    specialization = "Surgery"


def test_serialize_vet_returns_api_contract():
    assert serialize_vet(FakeVet()) == {
        "id": 1,
        "name": "Dr. Smith",
        "specialization": "Surgery",
    }


def test_list_vets_queries_and_serializes_items():
    class FakeQuery:
        def all(self):
            return [FakeVet()]

    class FakeDB:
        def query(self, model):
            self.model = model
            return FakeQuery()

    assert list_vets(FakeDB()) == [
        {
            "id": 1,
            "name": "Dr. Smith",
            "specialization": "Surgery",
        }
    ]
