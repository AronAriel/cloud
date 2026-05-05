from fastapi import FastAPI
from db import SessionLocal
from models import Feedback
from azure.servicebus import ServiceBusClient
import threading
import time
import logging


from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
logger = logging.getLogger(__name__)


QUEUE_NAME = os.getenv("QUEUE_NAME")
RECEIVE_CONNECTION_STRING = os.getenv("RECEIVE_CONNECTION_STRING")

app = FastAPI()




@app.get("/feedbacks")
def get_feedbacks():
    logger.info("Fetching feedbacks")

    db = SessionLocal()
    feedbacks = db.query(Feedback).all()

    logger.info(f"Found {len(feedbacks)} feedbacks")

    return [
        {
            "id": f.id,
            "consultation_id": f.consultation_id,
            "rating": f.rating,
            "comment": f.comment
        }
        for f in feedbacks
    ]
def receive_messages():
    try:
        logger.info("Starting Service Bus listener...")

        with ServiceBusClient.from_connection_string(RECEIVE_CONNECTION_STRING) as client:
            with client.get_queue_receiver(
                queue_name=QUEUE_NAME,
                max_wait_time=30  # longer wait
            ) as receiver:

                while True:
                    logger.info("Polling messages...")

                    messages = receiver.receive_messages(max_message_count=10)

                    if not messages:
                        logger.info("No messages received")
                        continue

                    for msg in messages:
                        logger.info(f"Received message: {msg}")
                        receiver.complete_message(msg)

    except Exception as e:
        logger.error(f"Error receiving messages: {e}")

@app.on_event("startup")
def start_background():
    logger.info("Starting Feedback Service...")

    thread = threading.Thread(target=receive_messages, daemon=True)
    thread.start()