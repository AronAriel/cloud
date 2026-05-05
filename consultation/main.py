from fastapi import FastAPI
from db import SessionLocal
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
from services import (
    create_consultation as create_consultation_service,
    list_consultations,
    send_service_bus_message,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()


class ConsultationCreate(BaseModel):
    pet_name: str
    date: str
    vet_id: int


def send_message(message: str):
    try:
        logger.info("Sending message to Service Bus")

        connection_string = os.getenv("SEND_CONNECTION_STRING")
        queue_name = os.getenv("QUEUE_NAME")

        if not connection_string or not queue_name:
            logger.warning("Service Bus settings are missing; message was not sent")
            return

        send_service_bus_message(connection_string, queue_name, message)

        logger.info("Message sent successfully")

    except Exception as e:
        logger.error(f"Error sending message: {e}")


@app.get("/consultations")
def get_consultations():
    logger.info("Fetching consultations")

    db = SessionLocal()

    try:
        consultations = list_consultations(db)
        logger.info(f"Found {len(consultations)} consultations")
        return consultations

    except Exception as e:
        logger.error(f"Error fetching consultations: {e}")
        raise
    finally:
        if hasattr(db, "close"):
            db.close()


@app.post("/consultations")
def create_consultation(data: ConsultationCreate):
    logger.info(f"Creating consultation for pet: {data.pet_name}")

    db = SessionLocal()

    try:
        result = create_consultation_service(db, data, send_message)
        logger.info("Consultation created")
        return result

    except Exception as e:
        logger.error(f"Error creating consultation: {e}")
        raise
    finally:
        if hasattr(db, "close"):
            db.close()


@app.on_event("startup")
def startup():
    logger.info("Consultation Service started")
