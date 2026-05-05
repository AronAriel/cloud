from azure.servicebus import ServiceBusClient, ServiceBusMessage

from models import Consultation


def serialize_consultation(consultation):
    return {
        "id": consultation.id,
        "pet_name": consultation.pet_name,
        "date": str(consultation.date),
        "vet_id": consultation.vet_id,
    }


def list_consultations(db):
    consultations = db.query(Consultation).all()
    return [serialize_consultation(item) for item in consultations]


def create_consultation(db, data, send_message):
    consultation = Consultation(
        pet_name=data.pet_name,
        date=data.date,
        vet_id=data.vet_id,
    )

    db.add(consultation)
    db.commit()

    send_message(f"New consultation created: {consultation.id}")

    return {"message": "created"}


def send_service_bus_message(connection_string, queue_name, message):
    with ServiceBusClient.from_connection_string(connection_string) as client:
        sender = client.get_queue_sender(queue_name=queue_name)
        with sender:
            sender.send_messages(ServiceBusMessage(message))
