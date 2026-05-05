from models import Vet


def serialize_vet(vet):
    return {
        "id": vet.id,
        "name": vet.name,
        "specialization": vet.specialization,
    }


def list_vets(db):
    vets = db.query(Vet).all()
    return [serialize_vet(vet) for vet in vets]
