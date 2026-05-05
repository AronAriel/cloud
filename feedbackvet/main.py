from fastapi import FastAPI
from db import SessionLocal
from azure.servicebus import ServiceBusClient
import threading
import logging
from services import consume_service_bus_messages, list_feedbacks


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
    try:
        feedbacks = list_feedbacks(db)
        logger.info(f"Found {len(feedbacks)} feedbacks")
        return feedbacks
    finally:
        if hasattr(db, "close"):
            db.close()


def receive_messages():
    try:
        if not RECEIVE_CONNECTION_STRING or not QUEUE_NAME:
            logger.warning("Service Bus settings are missing; listener was not started")
            return

        logger.info("Starting Service Bus listener...")

        with ServiceBusClient.from_connection_string(RECEIVE_CONNECTION_STRING) as client:
            with client.get_queue_receiver(
                queue_name=QUEUE_NAME,
                max_wait_time=30  # longer wait
            ) as receiver:

                while True:
                    logger.info("Polling messages...")

                    count = consume_service_bus_messages(receiver, logger)
                    if count == 0:
                        logger.info("No messages received")

    except Exception as e:
        logger.error(f"Error receiving messages: {e}")

@app.on_event("startup")
def start_background():
    logger.info("Starting Feedback Service...")

    thread = threading.Thread(target=receive_messages, daemon=True)
    thread.start()
