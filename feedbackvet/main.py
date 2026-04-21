from fastapi import FastAPI
from db import SessionLocal
from models import Feedback

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