from fastapi import FastAPI
from db import SessionLocal
from models import Consultation
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
logger = logging.getLogger(__name__)

SEND_CONNECTION_STRING = os.getenv("SEND_CONNECTION_STRING")
QUEUE_NAME = os.getenv("QUEUE_NAME")

app = FastAPI()



conn_str = os.getenv("SEND_CONNECTION_STRING")
queue_name = os.getenv("QUEUE_NAME")

with ServiceBusClient.from_connection_string(conn_str) as client:
    sender = client.get_queue_sender(queue_name=queue_name)
    with sender:
        sender.send_messages(ServiceBusMessage("New feedback created"))


class ConsultationCreate(BaseModel):
    pet_name: str
    date: str
    vet_id: int


def send_message(message: str):
    try:
        logger.info("Sending message to Service Bus")

        with ServiceBusClient.from_connection_string(SEND_CONNECTION_STRING) as client:
            sender = client.get_queue_sender(queue_name=QUEUE_NAME)
            with sender:
                sender.send_messages(ServiceBusMessage(message))

        logger.info("Message sent successfully")

    except Exception as e:
        logger.error(f"Error sending message: {e}")


@app.get("/consultations")
def get_consultations():
    logger.info("Fetching consultations")

    db = SessionLocal()

    try:
        consultations = db.query(Consultation).all()
        logger.info(f"Found {len(consultations)} consultations")

        return [
            {
                "id": c.id,
                "pet_name": c.pet_name,
                "date": str(c.date),
                "vet_id": c.vet_id
            }
            for c in consultations
        ]

    except Exception as e:
        logger.error(f"Error fetching consultations: {e}")
        raise


@app.post("/consultations")
def create_consultation(data: ConsultationCreate):
    logger.info(f"Creating consultation for pet: {data.pet_name}")

    db = SessionLocal()

    try:
        new_item = Consultation(
            pet_name=data.pet_name,
            date=data.date,
            vet_id=data.vet_id
        )

        db.add(new_item)
        db.commit()

        logger.info(f"Consultation created with id={new_item.id}")

        send_message(f"New consultation created: {new_item.id}")

        return {"message": "created"}

    except Exception as e:
        logger.error(f"Error creating consultation: {e}")
        raise


@app.on_event("startup")
def startup():
    logger.info("Consultation Service started")