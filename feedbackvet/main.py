from fastapi import FastAPI
from db import SessionLocal
from models import Feedback
from azure.servicebus import ServiceBusClient
import threading
import time


from dotenv import load_dotenv
import os

load_dotenv()

QUEUE_NAME = os.getenv("QUEUE_NAME")
RECEIVE_CONNECTION_STRING = os.getenv("RECEIVE_CONNECTION_STRING")

app = FastAPI()

@app.get("/feedbacks")
def get_feedbacks():
    db = SessionLocal()
    feedbacks = db.query(Feedback).all()

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
    while True:
        print("Listening...")

        with ServiceBusClient.from_connection_string(RECEIVE_CONNECTION_STRING) as client:
            receiver = client.get_queue_receiver(
                queue_name=QUEUE_NAME,
                max_wait_time=5
            )

            with receiver:
                messages = receiver.receive_messages(max_message_count=10)

                for msg in messages:
                    print("Received:", str(msg))
                    receiver.complete_message(msg)

        time.sleep(5)

@app.on_event("startup")
def start_background():
    thread = threading.Thread(target=receive_messages, daemon=True)
    thread.start()