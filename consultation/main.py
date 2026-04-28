from fastapi import FastAPI
from db import SessionLocal
from models import Consultation
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

SEND_CONNECTION_STRING = os.getenv("SEND_CONNECTION_STRING")
QUEUE_NAME = os.getenv("QUEUE_NAME")


app = FastAPI()
class ConsultationCreate(BaseModel):
    pet_name: str
    date: str
    vet_id: int


def send_message(message: str):
    with ServiceBusClient.from_connection_string(SEND_CONNECTION_STRING) as client:
        sender = client.get_queue_sender(queue_name=QUEUE_NAME)
        with sender:
            sender.send_messages(ServiceBusMessage(message))




@app.get("/consultations")
def get_consultations():
    db = SessionLocal()
    consultations = db.query(Consultation).all()

    return [
        {
            "id": c.id,
            "pet_name": c.pet_name,
            "date": str(c.date),
            "vet_id": c.vet_id
        }
        for c in consultations
    ]

@app.post("/consultations")
def create_consultation(data: ConsultationCreate):
    db = SessionLocal()

    new_item = Consultation(
        pet_name=data.pet_name,
        date=data.date,
        vet_id=data.vet_id
    )

    db.add(new_item)
    db.commit()

    send_message(f"New consultation created: {new_item.id}")

    return {"message": "created"}